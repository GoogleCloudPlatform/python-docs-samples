#include <cstdint>
#include <cstring>
#include <string>

#include "base/raw_logging.h"
#include "cloud/security/hawksbill/cavium/cavium_api_error.h"
#include "cloud/security/hawksbill/cavium/cavium_api_error_enum.h"
#include "cloud/security/hawksbill/cavium/cavium_api_interface.h"
#include "cloud/security/hawksbill/cavium/cavium_api_shim.h"
#include "experimental/users/brandonluong/cfmwrap/hsm_functions.h"
#include "testing/base/public/gmock.h"
#include "testing/base/public/gunit.h"
#include "third_party/absl/strings/string_view.h"

namespace third_party_cavium_hsm {
namespace {

using ::testing::Eq;
using ::testing::HasSubstr;
using ::testing::status::StatusIs;

third_party_cavium_interface::WrapArguments SetWrapArgumentsInputs(
    uint32_t session_handle, uint32_t wrapping_key_handle,
    uint32_t target_key_handle, uint32_t aes_key_wrap_pad) {
  third_party_cavium_interface::WrapArguments pArgs{};
  // inputs
  pArgs.common.session_handle = session_handle;
  pArgs.common.wrapping_key_handle = wrapping_key_handle;
  pArgs.common.mech = aes_key_wrap_pad;
  pArgs.common.key.ul_key_handle = target_key_handle;
  pArgs.common.key_input_output =
      third_party_cavium_interface::CaviumInputType::CAVIUM_ENCRYPTED;

  return pArgs;
}

// Set wrapped_key_len to length 8 and buffer length to 8192. Cavium returns a
// buffer too small error.
TEST(CfmWrapWrappedKeyLength, WrappedKeyLenSmallerThanWrappedKey) {
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  absl::StatusOr<uint32_t> target_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  uint32_t aes_key_wrap_pad = 0x00001091;

  third_party_cavium_interface::WrapArguments pArgs =
      SetWrapArgumentsInputs(session_handle, wrapping_key_handle,
                             target_key_handle.value(), aes_key_wrap_pad);

  // output args for CfmWrap
  uint8_t buffer[8912];  // as hardcoded in Cfm2Util
  pArgs.wrapped_key = buffer;
  // Set wrapped_key_len to minimum value of 8 to see if an error is returned.
  pArgs.wrapped_key_len = 8;

  ABSL_RAW_LOG(INFO, "wrapped_key_len before wrap: %lu",
               sizeof(pArgs.wrapped_key_len));

  uint64_t status = CaviumCfmWrap(&pArgs);
  // EXPECT_EQ(status, 0);
  ABSL_RAW_LOG(INFO, "Cavium Return Status: %lu", status);
  absl::Status status_error =
      hawksbill::cavium::CaviumApiShim::CaviumStatus(status, "CfmWrap");

  EXPECT_THAT(
      status_error,
      StatusIs(
          hawksbill::cavium::CaviumErrorSpace::Get(),
          Eq(third_party_cavium_interface::CaviumErrorCode::kErrBufferTooSmall),
          HasSubstr("ERR_BUFFER_TOO_SMALL")));
  ABSL_RAW_LOG(INFO, "buffer_before_cast size: %lu", sizeof(pArgs.wrapped_key));

  std::string output_key =
      reinterpret_cast<char *>(const_cast<uint8_t *>(pArgs.wrapped_key));
  ABSL_RAW_LOG(INFO, "output_key: %s \n buffer_after_cast size : %zul",
               output_key.c_str(), sizeof(output_key));

  std::vector<uint8_t> wrapped_key_vector(output_key.begin(), output_key.end());

  ABSL_RAW_LOG(INFO, "wrapped_key_len after wrap: %lu",
               sizeof(pArgs.wrapped_key_len));

  DeleteKey(session_handle, target_key_handle.value());
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}

// Set wrapped_key_len to 8000 and buffer length to 8192. The key was able to be
// wrapped and unwrapped successfully. wrapped_key_len was modified from 8000
// to 40. NOTE: Sometimes this will randomly fail.
TEST(CfmWrapWrappedKeyLength, WrappedKeyLenSmallerThanBufferSize) {
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  absl::StatusOr<uint32_t> target_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  uint32_t aes_key_wrap_pad = 0x00001091;

  third_party_cavium_interface::WrapArguments pArgs =
      SetWrapArgumentsInputs(session_handle, wrapping_key_handle,
                             target_key_handle.value(), aes_key_wrap_pad);

  // output args for CfmWrap
  uint8_t buffer[8912];  // as hardcoded in Cfm2Util
  pArgs.wrapped_key = buffer;
  // Set wrapped_key_len to length less than buffer.
  pArgs.wrapped_key_len = 8000;
  int wrapped_key_len_original = pArgs.wrapped_key_len;

  ABSL_RAW_LOG(INFO, "wrapped_key_len before wrap: %lu",
               sizeof(pArgs.wrapped_key_len));

  uint64_t status = CaviumCfmWrap(&pArgs);
  EXPECT_EQ(status, 0);
  ABSL_RAW_LOG(INFO, "Cavium Return Status: %lu", status);
  EXPECT_OK(hawksbill::cavium::CaviumApiShim::CaviumStatus(status, "CfmWrap"));
  ABSL_RAW_LOG(INFO, "buffer_before_cast size: %lu", sizeof(pArgs.wrapped_key));

  std::string output_key =
      reinterpret_cast<char *>(const_cast<uint8_t *>(pArgs.wrapped_key));
  ABSL_RAW_LOG(INFO, "output_key: %s \n buffer_after_cast size : %zul",
               output_key.c_str(), sizeof(output_key));

  EXPECT_NE(wrapped_key_len_original, pArgs.wrapped_key_len);
  ABSL_RAW_LOG(INFO, "wrapped_key_len_original: %d", wrapped_key_len_original);
  ABSL_RAW_LOG(INFO, "wrapped_key_len_after: %d", pArgs.wrapped_key_len);

  std::vector<uint8_t> wrapped_key_vector(output_key.begin(), output_key.end());

  // Wrapped key is able to be successfully unwrapped. Note that the unwrapped
  // target key handle can be different from the handle after creation.
  ASSERT_OK_AND_ASSIGN(
      target_key_handle,
      UnwrapKeyAesKwp(session_handle, wrapping_key_handle, wrapped_key_vector,
                      SymmetricKeyType::kAes256));

  DeleteKey(session_handle, target_key_handle.value());
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}

// Using a buffer with a size that is less than the wrapped key size will result
// in a segmentation fault.
TEST(CfmWrapWrappedKeyLength, BufferLessThanWrappedKeySize) {
  // uint32_t app_handle = Initialize();
  // uint32_t session_handle = OpenSession(app_handle);
  // uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  // absl::StatusOr<uint32_t> target_key_handle =
  // GenerateExtractableSymmetricKey(
  //     session_handle, SymmetricKeyType::kAes256);
  // // uint32_t aes_key_wrap_pad = 0x00001091;

  // WrapKeySmallBuffer(session_handle, wrapping_key_handle,
  //                    target_key_handle.value(), 8192);

  // third_party_cavium_interface::WrapArguments pArgs =
  //     SetWrapArgumentsInputs(session_handle, wrapping_key_handle,
  //                            target_key_handle.value(),
  //                            aes_key_wrap_pad);

  // output args for CfmWrap
  // Set buffer to minimum length of 8.
  // uint8_t buffer[8];  // as hardcoded in Cfm2Util
  // pArgs.wrapped_key = buffer;
  // pArgs.wrapped_key_len = 8192;
  // int wrapped_key_len_original = pArgs.wrapped_key_len;

  // ABSL_RAW_LOG(INFO, "wrapped_key_len_original before wrap: %d",
  //              wrapped_key_len_original);

  // uint64_t status = CaviumCfmWrap(&pArgs);
  // EXPECT_EQ(status, 0);
  // ABSL_RAW_LOG(INFO, "Cavium Return Status: %lu", status);
  // absl::Status status_error =
  //     hawksbill::cavium::CaviumApiShim::CaviumStatus(status, "CfmWrap");
  // EXPECT_OK(hawksbill::cavium::CaviumApiShim::CaviumStatus(status,
  // "CfmWrap"));
}

// Try swapping target and wrapping key. They target and wrapping keys have
// differerent permissions.
TEST(CfmWrapm, SwapTargetKeyAndWrappingKeyDistinctPermissions) {
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);

  absl::StatusOr<uint32_t> target_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  uint32_t aes_key_wrap_pad = 0x00001091;
  // uint32_t aes_key_wrap = 0x00001090;

  // swap target and wrapping key handles.
  third_party_cavium_interface::WrapArguments pArgs =
      SetWrapArgumentsInputs(session_handle, target_key_handle.value(),
                             wrapping_key_handle, aes_key_wrap_pad);

  // output args for CfmWrap
  uint8_t buffer[8924];  // as hardcoded in Cfm2Util
  pArgs.wrapped_key = buffer;
  pArgs.wrapped_key_len = sizeof(buffer);

  ABSL_RAW_LOG(INFO, "wrapped_key_len before wrap: %d", pArgs.wrapped_key_len);

  uint64_t status = CaviumCfmWrap(&pArgs);
  EXPECT_NE(status, 0);
  ABSL_RAW_LOG(INFO, "Cavium Return Status: %lu", status);
  absl::Status status_error =
      hawksbill::cavium::CaviumApiShim::CaviumStatus(status, "CfmWrap");
  EXPECT_THAT(
      status_error,
      StatusIs(
          hawksbill::cavium::CaviumErrorSpace::Get(),
          Eq(third_party_cavium_interface::CaviumErrorCode::kRetPolicyMismatch),
          HasSubstr(
              "This operation violates the current configured/FIPS policies")));
  ABSL_RAW_LOG(INFO, "buffer_before_cast size: %lu", sizeof(pArgs.wrapped_key));

  std::vector<uint8_t> wrapped_key(pArgs.wrapped_key,
                                   pArgs.wrapped_key + pArgs.wrapped_key_len);

  ABSL_RAW_LOG(INFO, "wraped key vector size: %lu", sizeof(wrapped_key));

  // AES_256_KEY_SIZE
  for (int i = 0; i < wrapped_key.size(); i++) {
    EXPECT_EQ(wrapped_key[i], pArgs.wrapped_key[i]);
  }

  std::string output_key =
      reinterpret_cast<char *>(const_cast<uint8_t *>(pArgs.wrapped_key));
  ABSL_RAW_LOG(INFO, "output_key: %s \n buffer_after_cast size : %zul",
               output_key.c_str(), sizeof(output_key));

  std::vector<uint8_t> wrapped_key_vector(output_key.begin(), output_key.end());

  ABSL_RAW_LOG(INFO, "wrapped_key_len after wrap: %d", pArgs.wrapped_key_len);

  DeleteKey(session_handle, target_key_handle.value());
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}

TEST(CfmWrapOutputLength,
     SwapTargetKeyAndWrappingKeySameExtractablePermissions) {
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  // wrapping key has same permissions as data key.
  uint32_t wrapping_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  absl::StatusOr<uint32_t> target_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  uint32_t aes_key_wrap_pad = 0x00001091;
  // uint32_t aes_key_wrap = 0x00001090;

  // swap target and wrapping key handles.
  third_party_cavium_interface::WrapArguments pArgs =
      SetWrapArgumentsInputs(session_handle, target_key_handle.value(),
                             wrapping_key_handle, aes_key_wrap_pad);

  // output args for CfmWrap
  uint8_t buffer[8924];  // as hardcoded in Cfm2Util
  pArgs.wrapped_key = buffer;
  pArgs.wrapped_key_len = sizeof(buffer);

  ABSL_RAW_LOG(INFO, "wrapped_key_len before wrap: %lu",
               sizeof(pArgs.wrapped_key_len));

  uint64_t status = CaviumCfmWrap(&pArgs);
  EXPECT_EQ(status, 0);
  ABSL_RAW_LOG(INFO, "Cavium Return Status: %lu", status);
  EXPECT_OK(hawksbill::cavium::CaviumApiShim::CaviumStatus(status, "CfmWrap"));
  ABSL_RAW_LOG(INFO, "buffer_before_cast size: %lu", sizeof(pArgs.wrapped_key));

  std::vector<uint8_t> wrapped_key(pArgs.wrapped_key,
                                   pArgs.wrapped_key + pArgs.wrapped_key_len);

  ABSL_RAW_LOG(INFO, "wraped key vector size: %lu", sizeof(wrapped_key));

  // AES_256_KEY_SIZE
  for (int i = 0; i < wrapped_key.size(); i++) {
    EXPECT_EQ(wrapped_key[i], pArgs.wrapped_key[i]);
  }

  std::string output_key =
      reinterpret_cast<char *>(const_cast<uint8_t *>(pArgs.wrapped_key));
  ABSL_RAW_LOG(INFO, "output_key: %s \n buffer_after_cast size : %zul",
               output_key.c_str(), sizeof(output_key));

  std::vector<uint8_t> wrapped_key_vector(output_key.begin(), output_key.end());

  ABSL_RAW_LOG(INFO, "wrapped_key_len after wrap: %lu",
               sizeof(pArgs.wrapped_key_len));

  // Wrapped key is able to be successfully unwrapped. Note that the unwrapped
  // target key handle can be different from the handle after creation.
  ASSERT_OK_AND_ASSIGN(
      target_key_handle,
      UnwrapKeyAesKwp(session_handle, target_key_handle.value(),
                      wrapped_key_vector, SymmetricKeyType::kAes256));

  DeleteKey(session_handle, target_key_handle.value());
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}

TEST(CfmWrapOutputLength, CheckLengthNoPad) {
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  absl::StatusOr<uint32_t> target_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  // uint32_t aes_key_wrap_pad = 0x00001091;
  uint32_t aes_key_wrap = 0x00001090;

  third_party_cavium_interface::WrapArguments pArgs =
      SetWrapArgumentsInputs(session_handle, wrapping_key_handle,
                             target_key_handle.value(), aes_key_wrap);

  constexpr int max_request_size = 8192;
  // output args for CfmWrap
  uint8_t buffer[max_request_size];  // as hardcoded in Cfm2Util
  pArgs.wrapped_key = buffer;
  pArgs.wrapped_key_len = max_request_size;

  uint64_t status = CaviumCfmWrap(&pArgs);
  EXPECT_EQ(status, 0);
  ABSL_RAW_LOG(INFO, "Cavium Return Status: %lu", status);
  EXPECT_OK(hawksbill::cavium::CaviumApiShim::CaviumStatus(status, "CfmWrap"));
  std::vector<uint8_t> wrapped_key(pArgs.wrapped_key,
                                   pArgs.wrapped_key + pArgs.wrapped_key_len);
  // AES_256_KEY_SIZE
  for (int i = 0; i < wrapped_key.size(); i++) {
    EXPECT_EQ(wrapped_key[i], pArgs.wrapped_key[i]);
  }

  absl::string_view output_key =
      reinterpret_cast<char *>(const_cast<uint8_t *>(pArgs.wrapped_key));
  ABSL_RAW_LOG(INFO, "output_key: %s \n output_key size : %zul",
               output_key.data(), output_key.size());

  // Wrapped key is able to be successfully unwrapped. Note that the unwrapped
  // target key handle can be different from the handle after creation.
  ASSERT_OK_AND_ASSIGN(target_key_handle,
                       UnwrapKeyAesKnp(session_handle, wrapping_key_handle,
                                       wrapped_key, SymmetricKeyType::kAes256));

  DeleteKey(session_handle, target_key_handle.value());
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}

TEST(CfmWrapOutputLength, CheckLengthWithPad) {
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  absl::StatusOr<uint32_t> target_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  uint32_t aes_key_wrap_pad = 0x00001091;
  // uint32_t aes_key_wrap = 0x00001090;

  third_party_cavium_interface::WrapArguments pArgs =
      SetWrapArgumentsInputs(session_handle, wrapping_key_handle,
                             target_key_handle.value(), aes_key_wrap_pad);

  // output args for CfmWrap
  uint8_t buffer[8924];  // as hardcoded in Cfm2Util
  pArgs.wrapped_key = buffer;
  pArgs.wrapped_key_len = sizeof(buffer);

  ABSL_RAW_LOG(INFO, "wrapped_key_len before wrap: %lu",
               sizeof(pArgs.wrapped_key_len));

  uint64_t status = CaviumCfmWrap(&pArgs);
  EXPECT_EQ(status, 0);
  ABSL_RAW_LOG(INFO, "Cavium Return Status: %lu", status);
  EXPECT_OK(hawksbill::cavium::CaviumApiShim::CaviumStatus(status, "CfmWrap"));
  ABSL_RAW_LOG(INFO, "buffer_before_cast size: %lu", sizeof(pArgs.wrapped_key));

  std::vector<uint8_t> wrapped_key(pArgs.wrapped_key,
                                   pArgs.wrapped_key + pArgs.wrapped_key_len);

  ABSL_RAW_LOG(INFO, "wraped key vector size: %lu", sizeof(wrapped_key));

  // AES_256_KEY_SIZE
  for (int i = 0; i < wrapped_key.size(); i++) {
    EXPECT_EQ(wrapped_key[i], pArgs.wrapped_key[i]);
  }

  std::string output_key =
      reinterpret_cast<char *>(const_cast<uint8_t *>(pArgs.wrapped_key));
  ABSL_RAW_LOG(INFO, "output_key: %s \n buffer_after_cast size : %zul",
               output_key.c_str(), sizeof(output_key));

  std::vector<uint8_t> wrapped_key_vector(output_key.begin(), output_key.end());

  ABSL_RAW_LOG(INFO, "wrapped_key_len after wrap: %lu",
               sizeof(pArgs.wrapped_key_len));

  // Wrapped key is able to be successfully unwrapped. Note that the unwrapped
  // target key handle can be different from the handle after creation.
  ASSERT_OK_AND_ASSIGN(
      target_key_handle,
      UnwrapKeyAesKwp(session_handle, wrapping_key_handle, wrapped_key_vector,
                      SymmetricKeyType::kAes256));

  DeleteKey(session_handle, target_key_handle.value());
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}

// This test is to check if the output wrapped material would have equal
// lengths. Ten target keys were generated and then wrapped. According to the
// logs most sizes are 401, but some are shorter.
TEST(CfmWrapOutoutLength, CheckIfWrappedKeyMaterialHasDistinctLength) {
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t aes_key_wrap_pad = 0x00001091;
  // uint32_t aes_key_wrap = 0x00001090;

  int wrapped_key_lengths[10];
  for (int i = 0; i < 10; i++) {
    uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
    absl::StatusOr<uint32_t> target_key_handle =
        GenerateExtractableSymmetricKey(session_handle,
                                        SymmetricKeyType::kAes256);
    third_party_cavium_interface::WrapArguments pArgs =
        SetWrapArgumentsInputs(session_handle, wrapping_key_handle,
                               target_key_handle.value(), aes_key_wrap_pad);

    // output args for CfmWrap
    uint8_t buffer[8192];  // as hardcoded in Cfm2Util
    pArgs.wrapped_key = buffer;
    pArgs.wrapped_key_len = sizeof(buffer);

    uint64_t status = CaviumCfmWrap(&pArgs);
    EXPECT_EQ(status, 0);
    ABSL_RAW_LOG(INFO, "Cavium Return Status: %lu", status);
    EXPECT_OK(
        hawksbill::cavium::CaviumApiShim::CaviumStatus(status, "CfmWrap"));

    std::vector<uint8_t> wrapped_key(pArgs.wrapped_key,
                                     pArgs.wrapped_key + pArgs.wrapped_key_len);

    auto char_wrapped_key =
        reinterpret_cast<char *>(const_cast<uint8_t *>(pArgs.wrapped_key));
    ABSL_RAW_LOG(INFO, "wrapped key: %s", char_wrapped_key);
    ABSL_RAW_LOG(INFO, "wrapped key: %lu", sizeof(char_wrapped_key));

    // AES_256_KEY_SIZE
    for (int i = 0; i < wrapped_key.size(); i++) {
      EXPECT_EQ(wrapped_key[i], pArgs.wrapped_key[i]);
      // ABSL_RAW_LOG(INFO, "%d", pArgs.wrapped_key[i]);
    }

    absl::string_view output_key =
        reinterpret_cast<char *>(const_cast<uint8_t *>(pArgs.wrapped_key));
    ABSL_RAW_LOG(INFO, "output_key: %s \n output_key size : %zul",
                 output_key.data(), output_key.size());
    wrapped_key_lengths[i] = output_key.size();
    DeleteKey(session_handle, target_key_handle.value());
    DeleteKey(session_handle, wrapping_key_handle);
  }

  for (int i = 0; i < 10; i++) {
    ABSL_RAW_LOG(INFO, "wrapped_key_lengths: %d \n ", wrapped_key_lengths[i]);
  }
  CloseSession(session_handle);
}

// Local testing for correctness of CaviumCfmWrap within
// cloud/security/hawksbill/cavium/cavium_api_interface.h
TEST(CaviumApiInterface, CfmWrapThenUnwrapSuccess) {
  // size fails at 8925, Cfm2Util hardcoded max is 8192
  uint8_t buffer[8924];  // as hardcoded in Cfm2Util
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  absl::StatusOr<uint32_t> target_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  uint32_t aes_key_wrap_pad = 0x00001091;

  third_party_cavium_interface::WrapArguments pArgs =
      SetWrapArgumentsInputs(session_handle, wrapping_key_handle,
                             target_key_handle.value(), aes_key_wrap_pad);

  // output args for CfmWrap
  pArgs.wrapped_key = buffer;
  pArgs.wrapped_key_len = sizeof(buffer);

  uint64_t status = CaviumCfmWrap(&pArgs);
  EXPECT_EQ(status, 0);
  ABSL_RAW_LOG(INFO, "Cavium Return Status: %lu", status);
  EXPECT_OK(hawksbill::cavium::CaviumApiShim::CaviumStatus(status, "CfmWrap"));
  std::vector<uint8_t> wrapped_key(pArgs.wrapped_key,
                                   pArgs.wrapped_key + pArgs.wrapped_key_len);
  for (int i = 0; i < wrapped_key.size(); i++) {
    EXPECT_EQ(wrapped_key[i], pArgs.wrapped_key[i]);
  }

  // Wrapped key is able to be successfully unwrapped. Note that the unwrapped
  // target key handle can be different from the handle after creation.
  ASSERT_OK_AND_ASSIGN(target_key_handle,
                       UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                       wrapped_key, SymmetricKeyType::kAes256));

  DeleteKey(session_handle, target_key_handle.value());
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}

// Local testing for correctness of CaviumCfmWrap within
// cloud/security/hawksbill/cavium/cavium_api_interface.h
TEST(CaviumApiInterface, RewrapFailsWithModifiedWrappedKey) {
  uint8_t buffer[8924];  // as hardcoded in Cfm2Util
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  absl::StatusOr<uint32_t> target_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  uint32_t aes_key_wrap_pad = 0x00001091;

  // target key handle saved for key deletion.
  uint32_t original_target_key_handle = target_key_handle.value();

  third_party_cavium_interface::WrapArguments pArgs =
      SetWrapArgumentsInputs(session_handle, wrapping_key_handle,
                             target_key_handle.value(), aes_key_wrap_pad);

  // output args for CfmWrap
  pArgs.wrapped_key = buffer;
  pArgs.wrapped_key_len = sizeof(buffer);

  uint64_t status = CaviumCfmWrap(&pArgs);
  EXPECT_EQ(status, 0);
  ABSL_RAW_LOG(INFO, "Cavium Return Status: %lu", status);
  EXPECT_OK(hawksbill::cavium::CaviumApiShim::CaviumStatus(status, "CfmWrap"));

  // Modify wrappedkey
  std::vector<uint8_t> wrapped_key(
      pArgs.wrapped_key, pArgs.wrapped_key + (pArgs.wrapped_key_len - 1));

  target_key_handle = UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                      wrapped_key, SymmetricKeyType::kAes256);

  // Rewrap fails due to modified key
  EXPECT_THAT(target_key_handle,
              testing::status::StatusIs(absl::StatusCode::kInternal));

  DeleteKey(session_handle, original_target_key_handle);
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}

// Testing CaviumShim layer
TEST(CaviumShim, CfmWrapThenUnwrapSuccess) {
  uint8_t buffer[8924];  // as hardcoded in Cfm2Util
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  absl::StatusOr<uint32_t> target_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  uint32_t aes_key_wrap_pad = 0x00001091;

  third_party_cavium_interface::WrapArguments pArgs =
      SetWrapArgumentsInputs(session_handle, wrapping_key_handle,
                             target_key_handle.value(), aes_key_wrap_pad);

  // output args
  pArgs.wrapped_key = buffer;
  pArgs.wrapped_key_len = sizeof(buffer);
  hawksbill::cavium::CaviumApiShim cavium_api_shim;
  uint64_t status = cavium_api_shim.CfmWrap(&pArgs);

  EXPECT_EQ(status, 0);
  ABSL_RAW_LOG(INFO, "Cavium Return Status: %lu", status);
  EXPECT_OK(hawksbill::cavium::CaviumApiShim::CaviumStatus(status, "CfmWrap"));
  std::vector<uint8_t> wrapped_key(pArgs.wrapped_key,
                                   pArgs.wrapped_key + pArgs.wrapped_key_len);
  for (int i = 0; i < wrapped_key.size(); i++) {
    EXPECT_EQ(wrapped_key[i], pArgs.wrapped_key[i]);
  }

  target_key_handle = UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                      wrapped_key, SymmetricKeyType::kAes256);

  ASSERT_OK_AND_ASSIGN(target_key_handle,
                       UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                       wrapped_key, SymmetricKeyType::kAes256));

  DeleteKey(session_handle, target_key_handle.value());
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}
TEST(CaviumShim, RewrapFailsWithModifiedWrappedKey) {
  uint8_t buffer[8924];  // as hardcoded in Cfm2Util
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  absl::StatusOr<uint32_t> target_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  uint32_t aes_key_wrap_pad = 0x00001091;

  uint32_t original_target_key_handle = target_key_handle.value();

  third_party_cavium_interface::WrapArguments pArgs =
      SetWrapArgumentsInputs(session_handle, wrapping_key_handle,
                             target_key_handle.value(), aes_key_wrap_pad);

  // output args
  pArgs.wrapped_key = buffer;
  pArgs.wrapped_key_len = sizeof(buffer);
  hawksbill::cavium::CaviumApiShim cavium_api_shim;
  uint64_t status = cavium_api_shim.CfmWrap(&pArgs);

  EXPECT_EQ(status, 0);
  ABSL_RAW_LOG(INFO, "Cavium Return Status: %lu", status);
  EXPECT_OK(hawksbill::cavium::CaviumApiShim::CaviumStatus(status, "CfmWrap"));

  // Modify wrappedkey
  std::vector<uint8_t> wrapped_key(
      pArgs.wrapped_key, pArgs.wrapped_key + (pArgs.wrapped_key_len - 1));

  target_key_handle = UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                      wrapped_key, SymmetricKeyType::kAes256);

  EXPECT_THAT(target_key_handle,
              testing::status::StatusIs(absl::StatusCode::kInternal));

  DeleteKey(session_handle, original_target_key_handle);
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}

}  // namespace
}  // namespace third_party_cavium_hsm