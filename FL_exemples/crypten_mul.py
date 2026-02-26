import crypten
import torch
from crypten.mpc import run_multiprocess


@run_multiprocess(world_size=2)
def demo_mpc_mul():
    rank = crypten.communicator.get().get_rank()
    if rank == 0:
        x_plain = torch.tensor([1.0, 2.0, 3.0])
        x = crypten.cryptensor(x_plain, src=0, precision=16)
        y = crypten.cryptensor(torch.empty(3), src=1, precision=16)
        print(f"Rank: {rank}, Tensor: {x_plain} ")
    else:
        # rank == 1
        y_plain = torch.tensor([10.0, 20.0, 30.0])
        y = crypten.cryptensor(y_plain, src=1, precision=16)
        x = crypten.cryptensor(torch.empty(3), src=0, precision=16)
        print(f"Rank: {rank}, Tensor: {y_plain} ")

    z = x * y
    z_decrypted = z.get_plain_text()
    print(f"[rank {rank}] decrypted result z = {z_decrypted}")


if __name__ == "__main__":
    demo_mpc_mul()
