from fastapi import APIRouter

router = APIRouter(
    tags=["Tasks"],
)

@router.get("/")
async def get_tasks():
    pass

@router.get("/{task_id}")
async def get_task(task_id: int):
    pass

@router.post("/")
async def post_task():
    pass

@router.put("/{task_id}")
async def put_task(task_id: int):
    pass

@router.patch("/{task_id}")
async def patch_task(task_id: int):
    pass

@router.delete("/{task_id}")
async def delete_task(task_id: int):
    pass