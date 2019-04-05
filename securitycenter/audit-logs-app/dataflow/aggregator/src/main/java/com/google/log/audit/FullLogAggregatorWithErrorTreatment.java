/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.google.log.audit;

import com.google.common.collect.Iterators;
import com.google.common.collect.Lists;
import com.google.gson.JsonParser;
import com.google.log.audit.common.PubsubTopicAndSubscriptionOptions;
import com.google.log.audit.common.WriteOneFilePerWindow;
import com.google.log.audit.mapper.AggregateFindingMapper;
import com.google.log.audit.mapper.MapperHelper;
import com.google.log.audit.validation.LogValidator;
import com.google.log.audit.validation.ValidationResponse;

import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.gcp.pubsub.PubsubIO;
import org.apache.beam.sdk.options.Default;
import org.apache.beam.sdk.options.Description;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.options.ValueProvider;
import org.apache.beam.sdk.options.Validation.Required;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.GroupByKey;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.transforms.windowing.FixedWindows;
import org.apache.beam.sdk.transforms.windowing.IntervalWindow;
import org.apache.beam.sdk.transforms.windowing.Window;
import org.apache.beam.sdk.values.KV;
import org.apache.beam.sdk.values.PCollectionTuple;
import org.apache.beam.sdk.values.TupleTag;
import org.apache.beam.sdk.values.TupleTagList;
import org.joda.time.Duration;

import java.util.List;

/**
 */
public class FullLogAggregatorWithErrorTreatment {

  private static final String SPLIT_TOKEN = "___###___";
  static final int DEFAULT_WINDOW_SIZE_IN_MINUTES = 60;
  static final int CHUNK_SIZE = 10;

  /**
   * Options supported by {@link FullLogAggregatorWithErrorTreatment}.
   *
   * <p>
   * Inherits standard configuration options.
   */
  public interface AggregateLogsOptions extends PubsubTopicAndSubscriptionOptions {

    @Description("Fixed window duration, in minutes")
    @Default.Integer(DEFAULT_WINDOW_SIZE_IN_MINUTES)
    Integer getWindowSize();

    void setWindowSize(Integer value);
    
    @Description("Max size of a chunck to aggregate.")
    @Default.Integer(CHUNK_SIZE)
    Integer getChunkSize();
    
    void setChunkSize(Integer value);

    @Description("The Cloud Pub/Sub topic to publish to. " + "The name should be in the format of "
        + "projects/<project-id>/topics/<topic-name>.")
    @Required
    ValueProvider<String> getOutputTopic();

    void setOutputTopic(ValueProvider<String> outputTopic);
    
    /** Set this required option to specify where to write the invalid findings. */
    @Description("Path of the file to write the invalid findings")
    @Required
    String getOutput();

    void setOutput(String value);
    
  }

  public static String getAssetIdFromLogString(String logInput) {
    JsonParser jsonParser = new JsonParser();
    return MapperHelper.normalizedResourceName(jsonParser.parse(logInput).getAsJsonObject());
  }

  static void runAggregateLogs(AggregateLogsOptions options) {
    Pipeline p = Pipeline.create(options);

    final TupleTag<String> validTag = new TupleTag<String>() {
    };
    final TupleTag<String> invalidTag = new TupleTag<String>() {
    };

    PCollectionTuple validatedInput = p
        .apply(PipelineSteps.READ_PUB_SUB.text,
            PubsubIO.readStrings().fromSubscription(options.getPubsubSubscription()))
        .apply(PipelineSteps.USE_FIXED_WINDOWS.text,
            Window.into(FixedWindows.of(Duration.standardMinutes(options.getWindowSize()))))
        .apply(PipelineSteps.VALIDATE_LOG_ITEMS.text, ParDo.of(new DoFn<String, String>() {

          @ProcessElement
          public void processElement(ProcessContext context, @Element String input) {
            ValidationResponse response = LogValidator.isValid(input);
            if (response.isValid()) {
              context.output(input);
            } else {
              context.output(invalidTag, response.getMessage() + " : " + input);
            }
          }
        }).withOutputTags(validTag, TupleTagList.of(invalidTag)));

    validatedInput.get(validTag).apply(PipelineSteps.CONVERT_TO_KVP.text, ParDo.of(convertStringLogToKV()))
        .apply(PipelineSteps.GROUP_KVP_BY_KEY.text, GroupByKey.<String, String>create())
        .apply(PipelineSteps.SPLIT_KVP_CHUNKS.text, ParDo.of(splitChunks()))
        .apply(PipelineSteps.CONVERT_KVP_TO_STRING.text, ParDo.of(convertKVToString()))
        .apply(PipelineSteps.WRITE_TO_PUB_SUB.text, PubsubIO.writeStrings().to(options.getOutputTopic()));

    validatedInput.get(invalidTag).apply(PipelineSteps.WRITE_INVALID_LOG_ITEMS.text,
        new WriteOneFilePerWindow(options.getOutput(), 1));

    p.run();
  }
  

  @SuppressWarnings("serial")
  private static DoFn<KV<String, Iterable<String>>, KV<String, Iterable<String>>> splitChunks() {
    return new DoFn<KV<String, Iterable<String>>, KV<String, Iterable<String>>>() {
      @ProcessElement
      public void proccessElement(@Element KV<String, Iterable<String>> input,
          OutputReceiver<KV<String, Iterable<String>>> output, PipelineOptions options) {
        int kvpSize = Iterators.size(input.getValue().iterator());
        int chunks = options.as(AggregateLogsOptions.class).getChunkSize();
        List<String> myList = Lists.newArrayList(input.getValue().iterator());
        if (kvpSize >= 1) {
          for (int i = 0; i < kvpSize; i += chunks) {
            KV<String, Iterable<String>> splitted;
            List<String> sublist = myList.subList(i, Math.min(kvpSize, i + chunks));
            Iterable<String> chunk = sublist;
            splitted = KV.of(input.getKey() + SPLIT_TOKEN + i, chunk);
            output.output(splitted);
          }
        }
      }
    };
  }

  @SuppressWarnings("serial")
  private static DoFn<KV<String, Iterable<String>>, String> convertKVToString() {
    return new DoFn<KV<String, Iterable<String>>, String>() {
      @ProcessElement
      public void proccessElement(@Element KV<String, Iterable<String>> input, OutputReceiver<String> output,
          IntervalWindow window) {
        String windowStart = window.start().toDateTime().toString();
        String windowEnd = window.end().toDateTime().toString();
        AggregateFindingMapper findingMapper = new AggregateFindingMapper(input.getValue(), windowStart, windowEnd);
        output.output(findingMapper.parse().build());
      }
    };
  }

  @SuppressWarnings("serial")
  private static DoFn<String, KV<String, String>> convertStringLogToKV() {
    return new DoFn<String, KV<String, String>>() {
      @ProcessElement
      public void processElement(@Element String logInput, OutputReceiver<KV<String, String>> keyValueOutput) {
        String assetId = getAssetIdFromLogString(logInput);
        keyValueOutput.output(KV.of(assetId, logInput));
      }
    };
  }

  public static void main(String[] args) {
    PipelineOptionsFactory.register(AggregateLogsOptions.class);
    AggregateLogsOptions options = PipelineOptionsFactory.fromArgs(args).withValidation().as(AggregateLogsOptions.class);

    runAggregateLogs(options);
  }

}
