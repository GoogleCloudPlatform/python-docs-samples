#ifndef EXPERIMENTAL_USERS_BRANDONLUONG_ASR_HSM_FUNCTIONS_H_
#define EXPERIMENTAL_USERS_BRANDONLUONG_ASR_HSM_FUNCTIONS_H_

#include <cstdint>
#include <vector>

#include "cloud/security/hawksbill/cavium/cavium_api_interface.h"
#include "third_party/absl/status/statusor.h"
#include "third_party/cavium_hsm/v3_4__14/cavium_structs.h"
#include "third_party/openssl/ec_key.h"
#include "third_party/openssl/rsa.h"

namespace third_party_cavium_hsm {

std::vector<uint8_t> RandomLabel();

uint32_t Test_Init();

uint32_t Initialize();
void Finalize(uint32_t application_handle);

uint32_t OpenSession(uint32_t application_handle);
void CloseSession(uint32_t session_handle);

uint64_t GenerateParkingKey(uint32_t session_handle);

void InitializeWrapArgs(third_party_cavium_interface::WrapArguments* pArgs);

uint64_t GenerateAesWrappingKey(uint32_t session_handle);

enum class SymmetricKeyType { kAes256, kHkdfSha256 };

uint64_t GenerateExtractableSymmetricKey(uint32_t session_handle,
                                         SymmetricKeyType key_type);

struct KeyPair {
  uint64_t pub;
  uint64_t prv;
};

KeyPair GenerateEcdhKeypair(uint32_t session_handle, int curve);

std::vector<uint8_t> ParkKey(uint32_t session_handle,
                             uint64_t parking_key_handle,
                             uint64_t target_key_handle);

uint64_t UnparkKey(uint32_t session_handle, uint64_t parking_key_handle,
                   std::vector<uint8_t>& parked_key);

std::vector<uint8_t> WrapKeyAesKwp(uint32_t session_handle,
                                   uint64_t wrapping_key_handle,
                                   uint64_t target_key_handle);

void WrapKeySmallBuffer(uint32_t session_handle, uint64_t wrapping_key_handle,
                        uint64_t target_key_handle, int wrapped_key_len);

uint64_t ImportRsaPublicKey(uint32_t session_handle, const RSA* rsa_pub);

std::vector<uint8_t> WrapKeyRsaOaep(uint32_t session_handle,
                                    uint64_t wrapping_key_handle,
                                    uint64_t target_key_handle);

absl::StatusOr<uint64_t> UnwrapKeyAesKwp(uint32_t session_handle,
                                         uint64_t wrapping_key_handle,
                                         std::vector<uint8_t>& wrapped_key,
                                         SymmetricKeyType key_type);

absl::StatusOr<uint64_t> UnwrapKeyAesKnp(uint32_t session_handle,
                                         uint64_t wrapping_key_handle,
                                         std::vector<uint8_t>& wrapped_key,
                                         SymmetricKeyType key_type);

uint64_t DeriveAes256KeyHkdfSha256(uint32_t session_handle, uint64_t key_handle,
                                   std::vector<uint8_t> info);

uint64_t DeriveAes256KeyEcdhHkdfSha256(uint32_t session_handle,
                                       uint64_t local_private_key_handle,
                                       EC_KEY* remote_public_key);

bssl::UniquePtr<EC_KEY> ExportEcPublicKey(uint32_t session_handle,
                                          uint64_t key_handle, int curve_id);

void DeleteKey(uint32_t session_handle, uint64_t key_handle);

}  // namespace third_party_cavium_hsm

#endif  // EXPERIMENTAL_USERS_BRANDONLUONG_ASR_HSM_FUNCTIONS_H_
