import torch
import crypten

crypten.init()
x = torch.tensor([10.0, 50.0, 100.0])
x_enc = crypten.cryptensor(x)
res = x_enc + x_enc
decrypted = res.get_plain_text()

print(f"Decrypted: {decrypted}")