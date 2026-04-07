# --- FIND ME ---

flag = "FLAG"
password = "hunter2"
api_key = "TEST-KEY-123"
secret = "classified"
token = "token_abcdef"

# --- ENTROPY TEST CASES ---

# High entropy (should trigger)
random_token = "a8F3kLm9QwXzP2rT7yU6vBnC0dEfGhIj"
super_random = "Z9xT$7qLp@2Vn8Wm#5Rk!YcH4Ue%3BfD"
jwt_like = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.KJHSD78sdf7sdf98sdf7sdf"
base64_blob = "QWxhZGRpbjpvcGVuIHNlc2FtZQ==ZXhhbXBsZQ=="

# Medium entropy (may or may not trigger depending on threshold)
mixed_string = "abc123XYZ789abc123XYZ"

# Low entropy (should NOT trigger)
normal_text = "this is just a normal sentence"
short_random = "a1b2c3"

# Edge case (long but repetitive → low entropy)
repeated = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"