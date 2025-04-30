
#include <cstdint>
#include <vector>

#include "experimental/users/brandonluong/cfmwrap/hsm_functions..h"
#include "testing/base/public/benchmark.h"
#include "testing/base/public/gunit.h"
#include "third_party/openssl/aes.h"
#include "third_party/openssl/base.h"
#include "third_party/openssl/bn.h"
#include "third_party/openssl/ec.h"
#include "third_party/openssl/ec_key.h"
#include "third_party/openssl/evp.h"
#include "third_party/openssl/nid.h"
#include "third_party/openssl/rsa.h"

namespace third_party_cavium_hsm {
namespace {

#define HSM_BENCHMARK(expr) BENCHMARK(expr)->Threads(8)->UseRealTime();

uint32_t application_handle;

// Initialize writes junk to stdout which makes the results unpretty, so make
// sure it only runs once.
void SetupGlobalState() { application_handle = Initialize(); }

void BM_ParkSymmetricKey(benchmark::State& state) {
  uint32_t session_handle = OpenSession(application_handle);

  uint64_t parking_key_handle = GenerateParkingKey(session_handle);
  uint64_t data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);

  for (auto s : state) {
    benchmark::DoNotOptimize(
        ParkKey(session_handle, parking_key_handle, data_key_handle));
  }

  DeleteKey(session_handle, data_key_handle);
  DeleteKey(session_handle, parking_key_handle);
  CloseSession(session_handle);

  state.SetItemsProcessed(state.iterations());
}

HSM_BENCHMARK(BM_ParkSymmetricKey);

void BM_WrapSymmetricKey(benchmark::State& state) {
  uint32_t session_handle = OpenSession(application_handle);

  uint64_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  uint64_t data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);

  for (auto s : state) {
    benchmark::DoNotOptimize(
        WrapKeyAesKwp(session_handle, wrapping_key_handle, data_key_handle));
  }

  DeleteKey(session_handle, data_key_handle);
  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);

  state.SetItemsProcessed(state.iterations());
}

HSM_BENCHMARK(BM_WrapSymmetricKey);

void BM_UnparkSymmetricKey(benchmark::State& state) {
  uint32_t session_handle = OpenSession(application_handle);

  uint64_t parking_key_handle = GenerateParkingKey(session_handle);
  uint64_t data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  std::vector<uint8_t> parked_key =
      ParkKey(session_handle, parking_key_handle, data_key_handle);
  DeleteKey(session_handle, data_key_handle);

  for (auto s : state) {
    data_key_handle = UnparkKey(session_handle, parking_key_handle, parked_key);
    DeleteKey(session_handle, data_key_handle);
  }

  DeleteKey(session_handle, parking_key_handle);
  CloseSession(session_handle);

  state.SetItemsProcessed(state.iterations());
}

HSM_BENCHMARK(BM_UnparkSymmetricKey);

void BM_UnwrapSymmetricKey(benchmark::State& state) {
  uint32_t session_handle = OpenSession(application_handle);

  uint64_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  uint64_t data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  std::vector<uint8_t> wrapped_key =
      WrapKeyAesKwp(session_handle, wrapping_key_handle, data_key_handle);
  DeleteKey(session_handle, data_key_handle);

  for (auto s : state) {
    data_key_handle = UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                      wrapped_key, SymmetricKeyType::kAes256);
    DeleteKey(session_handle, data_key_handle);
  }

  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);

  state.SetItemsProcessed(state.iterations());
}

HSM_BENCHMARK(BM_UnwrapSymmetricKey);

void GenerateAndWrapSymmetric(benchmark::State& state,
                              SymmetricKeyType key_type) {
  uint32_t session_handle = OpenSession(application_handle);
  uint64_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);

  for (auto s : state) {
    uint64_t data_key_handle = GenerateExtractableSymmetricKey(
        session_handle, SymmetricKeyType::kAes256);

    benchmark::DoNotOptimize(
        WrapKeyAesKwp(session_handle, wrapping_key_handle, data_key_handle));

    DeleteKey(session_handle, data_key_handle);
  }

  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);

  state.SetItemsProcessed(state.iterations());
}

void BM_GenerateAndWrapAes256(benchmark::State& state) {
  GenerateAndWrapSymmetric(state, SymmetricKeyType::kAes256);
}

HSM_BENCHMARK(BM_GenerateAndWrapAes256);

void BM_GenerateAndWrapHkdfSha256(benchmark::State& state) {
  GenerateAndWrapSymmetric(state, SymmetricKeyType::kHkdfSha256);
}

HSM_BENCHMARK(BM_GenerateAndWrapHkdfSha256);

void BM_UnwrapAes256(benchmark::State& state) {
  uint32_t session_handle = OpenSession(application_handle);
  uint64_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);

  uint64_t data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  std::vector<uint8_t> wrapped_key =
      WrapKeyAesKwp(session_handle, wrapping_key_handle, data_key_handle);
  DeleteKey(session_handle, data_key_handle);

  for (auto s : state) {
    data_key_handle = UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                      wrapped_key, SymmetricKeyType::kAes256);

    DeleteKey(session_handle, data_key_handle);
  }

  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);

  state.SetItemsProcessed(state.iterations());
}

HSM_BENCHMARK(BM_UnwrapAes256);

void BM_UnwrapAndDeriveHkdfSha256(benchmark::State& state) {
  uint32_t session_handle = OpenSession(application_handle);
  uint64_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);

  uint64_t derivation_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kHkdfSha256);
  std::vector<uint8_t> wrapped_key =
      WrapKeyAesKwp(session_handle, wrapping_key_handle, derivation_key_handle);
  DeleteKey(session_handle, derivation_key_handle);

  for (auto s : state) {
    derivation_key_handle =
        UnwrapKeyAesKwp(session_handle, wrapping_key_handle, wrapped_key,
                        SymmetricKeyType::kHkdfSha256);

    uint64_t data_key_handle = DeriveAes256KeyHkdfSha256(
        session_handle, derivation_key_handle, RandomLabel());

    DeleteKey(session_handle, derivation_key_handle);
    DeleteKey(session_handle, data_key_handle);
  }

  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);

  state.SetItemsProcessed(state.iterations());
}

HSM_BENCHMARK(BM_UnwrapAndDeriveHkdfSha256);

void UnwrapAesKwpRewrapRsa(benchmark::State& state, int rsa_bits) {
  bssl::UniquePtr<BIGNUM> f4(BN_new());
  CHECK_EQ(BN_set_u64(f4.get(), RSA_F4), 1);
  bssl::UniquePtr<RSA> rsa(RSA_new());
  CHECK_EQ(RSA_generate_key_ex(rsa.get(), rsa_bits, f4.get(), nullptr), 1);

  uint32_t session_handle = OpenSession(application_handle);

  uint64_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  uint64_t data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  std::vector<uint8_t> wrapped_key =
      WrapKeyAesKwp(session_handle, wrapping_key_handle, data_key_handle);
  DeleteKey(session_handle, data_key_handle);

  for (auto s : state) {
    data_key_handle = UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                      wrapped_key, SymmetricKeyType::kAes256);
    uint64_t public_key_handle = ImportRsaPublicKey(session_handle, rsa.get());

    benchmark::DoNotOptimize(
        WrapKeyRsaOaep(session_handle, public_key_handle, data_key_handle));

    DeleteKey(session_handle, public_key_handle);
    DeleteKey(session_handle, data_key_handle);
  }

  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);

  state.SetItemsProcessed(state.iterations());
}

void BM_UnwrapAesKwpRewrapRsa3072(benchmark::State& state) {
  UnwrapAesKwpRewrapRsa(state, 3072);
}

HSM_BENCHMARK(BM_UnwrapAesKwpRewrapRsa3072);

void BM_UnwrapAesKwpRewrapRsa4096(benchmark::State& state) {
  UnwrapAesKwpRewrapRsa(state, 4096);
}

HSM_BENCHMARK(BM_UnwrapAesKwpRewrapRsa4096);

void UnwrapAesKwpRewrapEcdh(benchmark::State& state, int curve_nid) {
  bssl::UniquePtr<EC_GROUP> group(EC_GROUP_new_by_curve_name(curve_nid));
  bssl::UniquePtr<EC_KEY> recipient_key(EC_KEY_new());
  CHECK_EQ(EC_KEY_set_group(recipient_key.get(), group.get()), 1);
  CHECK_EQ(EC_KEY_generate_key_fips(recipient_key.get()), 1);

  uint32_t session_handle = OpenSession(application_handle);

  KeyPair sender_handles = GenerateEcdhKeypair(session_handle, curve_nid);

  // Assume this is done at HSM startup or something like that, rather than
  // in band in each data plane operation.
  bssl::UniquePtr<EC_KEY> agree_pub_key =
      ExportEcPublicKey(session_handle, sender_handles.pub, curve_nid);

  uint64_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  uint64_t data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  std::vector<uint8_t> wrapped_key =
      WrapKeyAesKwp(session_handle, wrapping_key_handle, data_key_handle);
  DeleteKey(session_handle, data_key_handle);

  for (auto s : state) {
    data_key_handle = UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                                      wrapped_key, SymmetricKeyType::kAes256);

    uint64_t derived_key_handle = DeriveAes256KeyEcdhHkdfSha256(
        session_handle, sender_handles.prv, recipient_key.get());

    benchmark::DoNotOptimize(
        WrapKeyAesKwp(session_handle, derived_key_handle, data_key_handle));

    DeleteKey(session_handle, derived_key_handle);
    DeleteKey(session_handle, data_key_handle);
  }

  DeleteKey(session_handle, wrapping_key_handle);
  DeleteKey(session_handle, sender_handles.pub);
  DeleteKey(session_handle, sender_handles.prv);
  CloseSession(session_handle);

  state.SetItemsProcessed(state.iterations());
}

void BM_UnwrapAesKwpRewrapEcdhP256(benchmark::State& state) {
  UnwrapAesKwpRewrapEcdh(state, NID_X9_62_prime256v1);
}

HSM_BENCHMARK(BM_UnwrapAesKwpRewrapEcdhP256);

void BM_UnwrapAesKwpRewrapEcdhP384(benchmark::State& state) {
  UnwrapAesKwpRewrapEcdh(state, NID_secp384r1);
}

HSM_BENCHMARK(BM_UnwrapAesKwpRewrapEcdhP384);

void BM_UnwrapAesKwpRewrapEcdhP521(benchmark::State& state) {
  UnwrapAesKwpRewrapEcdh(state, NID_secp521r1);
}

HSM_BENCHMARK(BM_UnwrapAesKwpRewrapEcdhP521);

void BM_ReencryptAesKwp(benchmark::State& state) {
  uint32_t session_handle = OpenSession(application_handle);

  uint64_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  uint64_t session_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  uint64_t data_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);

  std::vector<uint8_t> wrapped_session_key =
      WrapKeyAesKwp(session_handle, wrapping_key_handle, session_key_handle);
  DeleteKey(session_handle, session_key_handle);

  std::vector<uint8_t> wrapped_data_key =
      WrapKeyAesKwp(session_handle, wrapping_key_handle, data_key_handle);
  DeleteKey(session_handle, data_key_handle);

  for (auto s : state) {
    session_key_handle =
        UnwrapKeyAesKwp(session_handle, wrapping_key_handle,
                        wrapped_session_key, SymmetricKeyType::kAes256);
    data_key_handle =
        UnwrapKeyAesKwp(session_handle, wrapping_key_handle, wrapped_data_key,
                        SymmetricKeyType::kAes256);

    benchmark::DoNotOptimize(
        WrapKeyAesKwp(session_handle, session_key_handle, data_key_handle));

    DeleteKey(session_handle, session_key_handle);
    DeleteKey(session_handle, data_key_handle);
  }

  DeleteKey(session_handle, wrapping_key_handle);
  CloseSession(session_handle);

  state.SetItemsProcessed(state.iterations());
}

HSM_BENCHMARK(BM_ReencryptAesKwp);

}  // namespace
}  // namespace third_party_cavium_hsm

int main(int argc, char** argv) {
  testing::InitGoogleTest(&argc, argv);
  third_party_cavium_hsm::SetupGlobalState();
  RunSpecifiedBenchmarks();
  return 0;
}