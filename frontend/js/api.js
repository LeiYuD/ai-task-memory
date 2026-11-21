// frontend/js/api.js

const BASE_URL = 'http://127.0.0.1:8000/api/v1';

// 获取所有候选任务
async function getCandidates() {
    const response = await fetch(`${BASE_URL}/tasks/candidates`);
    if (!response.ok) throw new Error('获取数据失败');
    return await response.json();
}

// 确认任务
async function confirmTaskById(id) {
    const response = await fetch(`${BASE_URL}/tasks/${id}/confirm`, {
        method: 'POST'
    });
    if (!response.ok) throw new Error('确认任务失败');
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