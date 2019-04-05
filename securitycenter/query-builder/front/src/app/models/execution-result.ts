export class ExecutionResult {
  scc_query_link: string;
  result_size: Number;
  mark: string;
  uuid: string;
  stepResult: any;

  constructor (scc_query_link, result_size, mark, uuid, stepResult) {
    this.scc_query_link = scc_query_link;
    this.result_size = result_size;
    this.mark = mark;
    this.uuid = uuid;
    this.stepResult = stepResult;
  }
}
