#include "experimental/users/brandonluong/cfmwrap/hsm_functions.h"

#include <cstdint>

#include "base/raw_logging.h"
#include "testing/base/public/gmock.h"
#include "testing/base/public/gunit.h"
#include "third_party/absl/log/log.h"
#include "third_party/absl/status/statusor.h"
#include "third_party/absl/strings/substitute.h"
#include "third_party/openssl/aes.h"
#include "third_party/openssl/base.h"
#include "third_party/openssl/bn.h"
#include "third_party/openssl/ec.h"
#include "third_party/openssl/ec_key.h"
#include "third_party/openssl/ecdh.h"
#include "third_party/openssl/evp.h"
#include "third_party/openssl/hkdf.h"
#include "third_party/openssl/rsa.h"

namespace third_party_cavium_hsm {
namespace {

TEST(HsmFunctionsTest, InitializeHSM) {
  uint32_t app_handle = Initialize();
  ABSL_RAW_LOG(INFO, "app_handle %d", app_handle);
  uint32_t session_handle = OpenSession(app_handle);

  // // uint32_t session_handle = OpenSession(app_handle);
  ABSL_RAW_LOG(INFO, "session handle : %d\n app handle: %d\n", session_handle,
               app_handle);
}

TEST(HsmFunctionsTest, GenerateParkUnparkAes256) {
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t parking_key_handle = GenerateParkingKey(session_handle);
  uint32_t data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);

  std::vector<uint8_t> parked_key =
      ParkKey(session_handle, parking_key_handle, data_key_handle);
  DeleteKey(session_handle, data_key_handle);

  data_key_handle = UnparkKey(session_handle, parking_key_handle, parked_key);

  DeleteKey(session_handle, data_key_handle);
  DeleteKey(session_handle, parking_key_handle);
  CloseSession(session_handle);
}

TEST(HsmFunctionsTest, GenerateParkUnparkHkdfSha256) {
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t parking_key_handle = GenerateParkingKey(session_handle);
  uint32_t derivation_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kHkdfSha256);

  std::vector<uint8_t> parked_key =
      ParkKey(session_handle, parking_key_handle, derivation_key_handle);
  DeleteKey(session_handle, derivation_key_handle);

  derivation_key_handle =
      UnparkKey(session_handle, parking_key_handle, parked_key);

  uint32_t data_key_handle = DeriveAes256KeyHkdfSha256(
      session_handle, derivation_key_handle, RandomLabel());

  DeleteKey(session_handle, data_key_handle);
  DeleteKey(session_handle, derivation_key_handle);
  DeleteKey(session_handle, parking_key_handle);
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

  third_party_cavium_interface::WrapArguments pArgs{};
  // input args for CfmWrap
  pArgs.common.session_handle = session_handle;
  pArgs.common.wrapping_key_handle = wrapping_key_handle;
  pArgs.common.mech = aes_key_wrap_pad;
  pArgs.common.key.ul_key_handle = target_key_handle.value();
  pArgs.common.key_input_output =
      third_party_cavium_interface::CaviumInputType::CAVIUM_ENCRYPTED;

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

  target_key_handle = UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                      wrapped_key, SymmetricKeyType::kAes256);

  // Wrapped key is able to be successfully unwrapped. Note that the unwrapped
  // target key handle can be different from the handle after creation.
  ASSERT_OK_AND_ASSIGN(target_key_handle,
                       UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                       wrapped_key, SymmetricKeyType::kAes256));

  DeleteKey(session_handle, target_key_handle.value());
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}
TEST(CaviumApiInterface, CreateWrappingKeyUnparkWrapUnwrap) {
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t parking_key_handle = GenerateParkingKey(session_handle);
  // Create wrapping key
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);

  // park wrapping key
  std::vector<uint8_t> parked_wrapping_key =
      ParkKey(session_handle, parking_key_handle, wrapping_key_handle);

  LOG(INFO) << absl::Substitute("parked_wrapping_key size: $0",
                                parked_wrapping_key.size());

  // unpark wrapping key
  uint32_t unparked_wrapping_key_handle =
      UnparkKey(session_handle, parking_key_handle, parked_wrapping_key);

  // create data key
  absl::StatusOr<uint32_t> data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);

  // wrap data key with wrapping key
  uint8_t buffer[8924];
  uint32_t aes_key_wrap_pad = 0x00001091;
  third_party_cavium_interface::WrapArguments pArgs{};
  // input args for CfmWrap
  pArgs.common.session_handle = session_handle;
  pArgs.common.wrapping_key_handle = unparked_wrapping_key_handle;
  pArgs.common.mech = aes_key_wrap_pad;
  pArgs.common.key.ul_key_handle = data_key_handle.value();
  pArgs.common.key_input_output =
      third_party_cavium_interface::CaviumInputType::CAVIUM_ENCRYPTED;
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

  ASSERT_OK_AND_ASSIGN(data_key_handle,
                       UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                       wrapped_key, SymmetricKeyType::kAes256));

  DeleteKey(session_handle, data_key_handle.value());
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

  third_party_cavium_interface::WrapArguments pArgs{};
  // input args for CfmWrap
  pArgs.common.session_handle = session_handle;
  pArgs.common.wrapping_key_handle = wrapping_key_handle;
  pArgs.common.mech = aes_key_wrap_pad;
  pArgs.common.key.ul_key_handle = target_key_handle.value();
  pArgs.common.key_input_output =
      third_party_cavium_interface::CaviumInputType::CAVIUM_ENCRYPTED;

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

  third_party_cavium_interface::WrapArguments pArgs{};

  // input args
  pArgs.common.session_handle = session_handle;
  pArgs.common.wrapping_key_handle = wrapping_key_handle;
  pArgs.common.mech = aes_key_wrap_pad;
  pArgs.common.key.ul_key_handle = target_key_handle.value();
  pArgs.common.key_input_output =
      third_party_cavium_interface::CaviumInputType::CAVIUM_ENCRYPTED;

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

TEST(Caviumshim, RewrapFailsWithModifiedWrappedKey) {
  uint8_t buffer[8924];  // as hardcoded in Cfm2Util
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  absl::StatusOr<uint32_t> target_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  uint32_t aes_key_wrap_pad = 0x00001091;

  uint32_t original_target_key_handle = target_key_handle.value();

  third_party_cavium_interface::WrapArguments pArgs{};

  // input args
  pArgs.common.session_handle = session_handle;
  pArgs.common.wrapping_key_handle = wrapping_key_handle;
  pArgs.common.mech = aes_key_wrap_pad;
  pArgs.common.key.ul_key_handle = target_key_handle.value();
  pArgs.common.key_input_output =
      third_party_cavium_interface::CaviumInputType::CAVIUM_ENCRYPTED;

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

  target_key_handle = UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                      wrapped_key, SymmetricKeyType::kAes256);

  EXPECT_THAT(target_key_handle,
              testing::status::StatusIs(absl::StatusCode::kInternal));

  DeleteKey(session_handle, original_target_key_handle);
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}

TEST(HsmFunctionsTest, GenerateWrapUnwrapAes256) {
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  uint32_t data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);

  std::vector<uint8_t> wrapped_key =
      WrapKeyAesKwp(session_handle, wrapping_key_handle, data_key_handle);
  DeleteKey(session_handle, data_key_handle);

  data_key_handle = UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                    wrapped_key, SymmetricKeyType::kAes256)
                        .value();

  DeleteKey(session_handle, data_key_handle);
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}

TEST(HsmFunctionsTest, GenerateWrapUnwrapHkdfSha256) {
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  uint32_t derivation_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);

  std::vector<uint8_t> wrapped_key =
      WrapKeyAesKwp(session_handle, wrapping_key_handle, derivation_key_handle);
  DeleteKey(session_handle, derivation_key_handle);

  derivation_key_handle =
      UnwrapKeyAesKwp(session_handle, wrapping_key_handle, wrapped_key,
                      SymmetricKeyType::kHkdfSha256)
          .value();

  uint32_t data_key_handle = DeriveAes256KeyHkdfSha256(
      session_handle, derivation_key_handle, RandomLabel());

  DeleteKey(session_handle, data_key_handle);
  DeleteKey(session_handle, derivation_key_handle);
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);
}

class RsaWrapTest : public testing::TestWithParam<int> {};

TEST_P(RsaWrapTest, RsaWrap) {
  int rsa_bits = GetParam();

  bssl::UniquePtr<BIGNUM> f4(BN_new());
  ASSERT_EQ(BN_set_u64(f4.get(), RSA_F4), 1);

  bssl::UniquePtr<RSA> rsa(RSA_new());
  ASSERT_EQ(RSA_generate_key_ex(rsa.get(), rsa_bits, f4.get(), nullptr), 1);

  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);

  uint32_t public_key_handle = ImportRsaPublicKey(session_handle, rsa.get());
  uint32_t data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);

  std::vector<uint8_t> wrapped_key =
      WrapKeyRsaOaep(session_handle, public_key_handle, data_key_handle);

  bssl::UniquePtr<EVP_PKEY> pkey(EVP_PKEY_new());
  ASSERT_EQ(EVP_PKEY_set1_RSA(pkey.get(), rsa.get()), 1);

  bssl::UniquePtr<EVP_PKEY_CTX> ctx(EVP_PKEY_CTX_new(pkey.get(), nullptr));
  ASSERT_EQ(EVP_PKEY_decrypt_init(ctx.get()), 1);
  ASSERT_EQ(EVP_PKEY_CTX_set_rsa_padding(ctx.get(), RSA_PKCS1_OAEP_PADDING), 1);
  ASSERT_EQ(EVP_PKEY_CTX_set_rsa_oaep_md(ctx.get(), EVP_sha256()), 1);
  ASSERT_EQ(EVP_PKEY_CTX_set_rsa_mgf1_md(ctx.get(), EVP_sha256()), 1);

  std::vector<uint8_t> recovered;
  recovered.resize(RSA_size(rsa.get()));
  size_t out_len = recovered.size();

  ASSERT_EQ(EVP_PKEY_decrypt(ctx.get(), recovered.data(), &out_len,
                             wrapped_key.data(), wrapped_key.size()),
            1);

  ASSERT_EQ(out_len, 32);

  DeleteKey(session_handle, data_key_handle);
  DeleteKey(session_handle, public_key_handle);
  CloseSession(session_handle);
}

INSTANTIATE_TEST_SUITE_P(RsaWrap, RsaWrapTest, testing::Values(3072, 4096));

class EcdhWrapTest : public testing::TestWithParam<int> {};

TEST_P(EcdhWrapTest, EcdhWrap) {
  int curve_nid = GetParam();

  bssl::UniquePtr<EC_GROUP> group(EC_GROUP_new_by_curve_name(curve_nid));
  bssl::UniquePtr<EC_KEY> ec(EC_KEY_new());
  ASSERT_EQ(EC_KEY_set_group(ec.get(), group.get()), 1);
  ASSERT_EQ(EC_KEY_generate_key_fips(ec.get()), 1);

  bssl::UniquePtr<EVP_PKEY> pkey(EVP_PKEY_new());
  ASSERT_EQ(EVP_PKEY_set1_EC_KEY(pkey.get(), ec.get()), 1);

  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);

  KeyPair durable_agree_key = GenerateEcdhKeypair(session_handle, curve_nid);

  uint32_t data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);

  uint32_t wrapping_key_handle = DeriveAes256KeyEcdhHkdfSha256(
      session_handle, durable_agree_key.prv, ec.get());

  std::vector<uint8_t> wrapped_key =
      WrapKeyAesKwp(session_handle, wrapping_key_handle, data_key_handle);

  bssl::UniquePtr<EC_KEY> agree_pub_key =
      ExportEcPublicKey(session_handle, durable_agree_key.pub, curve_nid);

  std::vector<uint8_t> shared_secret;
  constexpr size_t kMaxSharedSecretBytes =
      66;  // == ceil(521 / 8) for P-521 key
  shared_secret.resize(kMaxSharedSecretBytes);

  int retrieved_bytes = ECDH_compute_key(
      shared_secret.data(), shared_secret.size(),
      EC_KEY_get0_public_key(agree_pub_key.get()), ec.get(), nullptr);
  CHECK_GE(retrieved_bytes, 32);
  shared_secret.resize(retrieved_bytes);

  std::vector<uint8_t> kwp_key;
  kwp_key.resize(32);
  ASSERT_EQ(
      HKDF(kwp_key.data(), kwp_key.size(), EVP_sha256(), shared_secret.data(),
           shared_secret.size(), nullptr, 0, nullptr, 0),
      1);

  AES_KEY k;
  ASSERT_EQ(AES_set_decrypt_key(kwp_key.data(), 256, &k), 0);

  std::vector<uint8_t> data_key;
  data_key.resize(32);
  size_t data_key_size = data_key.size();
  ASSERT_EQ(AES_unwrap_key_padded(&k, data_key.data(), &data_key_size,
                                  data_key.size(), wrapped_key.data(),
                                  wrapped_key.size()),
            1);

  DeleteKey(session_handle, wrapping_key_handle);
  DeleteKey(session_handle, data_key_handle);
  DeleteKey(session_handle, durable_agree_key.pub);
  DeleteKey(session_handle, durable_agree_key.prv);

  CloseSession(session_handle);
}

INSTANTIATE_TEST_SUITE_P(EcdhWrap, EcdhWrapTest,
                         testing::Values(NID_X9_62_prime256v1, NID_secp384r1,
                                         NID_secp521r1));

}  // namespace
}  // namespace third_party_cavium_hsm