import torch
import torch.distributed as dist


def init_distributed(rank, world_size):
    if dist.is_initialized():
        return None

    dist.init_process_group(
        backend="gloo",
        init_method="tcp://127.0.0.1:29500",
        rank=rank,
        world_size=world_size,
    )


def run(rank, world_size=1):
    init_distributed(rank, world_size)
    tensor_size = 4
    if rank == 0:
        # На процессе 0 создаем тензор для отправки
        tensor = torch.arange(tensor_size, dtype=torch.long)
        print(f"Rank {rank}: source tensor = {tensor}")
    else:
        # На других процессах создаем пустой тензор
        tensor = torch.zeros(tensor_size, dtype=torch.long)
        print(f"Rank {rank}: tensor before broadcast = {tensor}")
    dist.broadcast(tensor, src=0)
    print(f"Rank {rank}: tensor after broadcast = {tensor}")



if __name__ == "__main__":
    try:
        run(0, world_size=1)
    finally:
        if dist.is_initialized():
            dist.destroy_process_group()
