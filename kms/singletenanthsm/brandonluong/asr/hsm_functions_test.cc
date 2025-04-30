#include "experimental/users/brandonluong/asr/hsm_functions.h"

#include <sys/types.h>

#include <cstdint>

#include "base/raw_logging.h"
#include "testing/base/public/gmock.h"
#include "testing/base/public/gunit.h"
#include "third_party/openssl/base.h"
#include "third_party/openssl/nid.h"

namespace third_party_cavium_hsm {
namespace {

TEST(HsmFunctionsTest, InitializeHSM) {
  uint32_t app_handle = Initialize();
  ABSL_RAW_LOG(INFO, "app_handle %d", app_handle);
  uint32_t session_handle = OpenSession(app_handle);

  ABSL_RAW_LOG(INFO, "session handle : %d\n app handle: %d\n", session_handle,
               app_handle);
}

// Test Parking and unparking DEK
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

TEST(HsmFunctionsTest, SymmetricRewrapWorkflowSuccess) {
  int curve_nid = NID_secp384r1;

  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t parking_key_handle = GenerateParkingKey(session_handle);

  // Create data encryption key(DEK).
  uint32_t data_encryption_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);

  // Create region B's Data Key Wrapping Key(DKWK).
  // Region A's DKWK would have already been used in CreateWrapDataKey and
  // RewrapDataKey. It is necessary for this workflow.
  uint64_t region_b_dkwk_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);

  // Park region B's DKWK.
  std::vector<uint8_t> region_b_parked_dkwk =
      ParkKey(session_handle, parking_key_handle, region_b_dkwk_handle);

  // Create 2 ECDH keys.
  KeyPair ecdh_key_region_a = GenerateEcdhKeypair(session_handle, curve_nid);
  KeyPair ecdh_key_region_b = GenerateEcdhKeypair(session_handle, curve_nid);

  // Convert public keys into EC form.
  // There will be 2 ECDH key pairs: one for region A and one for region B.
  bssl::UniquePtr<EC_KEY> region_a_pub_key =
      ExportEcPublicKey(session_handle, ecdh_key_region_a.pub, curve_nid);
  bssl::UniquePtr<EC_KEY> region_b_pub_key =
      ExportEcPublicKey(session_handle, ecdh_key_region_b.pub, curve_nid);

  // Derive the shared secret using (priA and pubB) or (priB and pubA).
  // Then use HKDF + ECDH to get each region's wrapping key.
  uint32_t region_a_wrapping_key_handle = DeriveAes256KeyEcdhHkdfSha256(
      session_handle, ecdh_key_region_a.prv, region_b_pub_key.get());
  uint32_t region_b_wrapping_key_handle = DeriveAes256KeyEcdhHkdfSha256(
      session_handle, ecdh_key_region_b.prv, region_a_pub_key.get());

  // Wrap the DEK with region A's ecdh + hkdf key.
  // This is the wrapped DEK from the output of RewrapDataKey. From here we can
  // start the workflow of SymmetricRewrap.
  std::vector<uint8_t> region_a_wrapped_dek = WrapKeyAesKwp(
      session_handle, region_a_wrapping_key_handle, data_encryption_key_handle);

  // Unwrap using region B's ecdh + hkdf key.
  // DEK that is wrapped with region a's shared secret is able to be unwrapped
  // by region b's shared secret. Note that the unwrapped DEK handle can be
  // different from the original DEK handle after creation.
  ASSERT_OK_AND_ASSIGN(
      data_encryption_key_handle,
      UnwrapKeyAesKwp(session_handle, region_b_wrapping_key_handle,
                      region_a_wrapped_dek, SymmetricKeyType::kAes256));

  // Unpark region B's DKWK
  uint64_t region_b_unparked_dkwk_handle =
      UnparkKey(session_handle, parking_key_handle, region_b_parked_dkwk);

  // Wrap the DEK with region B's DKWK.
  // This is the output of SymmetricRewrap. The DEK is wrapped within region
  // b's DKWK. The DKWK is an AES 256 key.
  std::vector<uint8_t> aes_wrapped_dek =
      WrapKeyAesKwp(session_handle, region_b_unparked_dkwk_handle,
                    data_encryption_key_handle);

  // Unwrap using region B's DKWK
  EXPECT_OK(UnwrapKeyAesKwp(session_handle, region_b_unparked_dkwk_handle,
                            aes_wrapped_dek, SymmetricKeyType::kAes256));

  DeleteKey(session_handle, region_b_unparked_dkwk_handle);
  DeleteKey(session_handle, region_b_wrapping_key_handle);
  DeleteKey(session_handle, region_a_wrapping_key_handle);
  DeleteKey(session_handle, data_encryption_key_handle);
  DeleteKey(session_handle, parking_key_handle);
  CloseSession(session_handle);
}

}  // namespace
}  // namespace third_party_cavium_hsm
