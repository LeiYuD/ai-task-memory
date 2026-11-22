// frontend/js/api.js

const BASE_URL = 'http://127.0.0.1:8000/api/v1';

// 获取所有候选任务
async function getCandidates() {
    const response = await fetch(`${BASE_URL}/tasks/candidates`);
    if (!response.ok) throw new Error('获取数据失败');
    return await response.json();
}

// 获取看板任务 (进行中)
async function getBoardTasks() {
    const response = await fetch(`${BASE_URL}/tasks/?status=IN_PROGRESS`);
    if (!response.ok) throw new Error('获取看板失败');
    return await response.json();
}

// 确认任务 (加入看板)
async function confirmTaskById(id) {
    const response = await fetch(`${BASE_URL}/tasks/${id}/confirm`, {
        method: 'POST'
    });
    if (!response.ok) throw new Error('确认任务失败');
    return await response.json();
}

// 标记任务完成
async function completeTaskById(id) {
    const response = await fetch(`${BASE_URL}/tasks/${id}/complete`, {
        method: 'POST'
    });
    if (!response.ok) throw new Error('标记完成失败');
    return await response.json();
}

// 删除/忽略任务
async function deleteTaskById(id) {
    const response = await fetch(`${BASE_URL}/tasks/${id}`, {
        method: 'DELETE'
    });
    if (!response.ok) throw new Error('删除失败');
    return await response.json();
}

// 人工改写任务
async function updateTask(id, taskData) {
    const response = await fetch(`${BASE_URL}/tasks/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(taskData)
    });
    if (!response.ok) throw new Error('改写失败');
    return await response.json();
}