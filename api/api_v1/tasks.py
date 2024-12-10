from fastapi import APIRouter

router = APIRouter(
    tags=["Tasks"],
)

@router.get("/")
async def get_tasks():
    return {"success": True, "result": []}

@router.post("/{task_id}")
async def post_task(task_id: int):
    return {"success": True, "result": {"task_id": task_id}}
