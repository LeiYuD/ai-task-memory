// frontend/js/api.js

const BASE_URL = 'http://127.0.0.1:8000/api/v1';

async function getCandidates() {
    const response = await fetch(`${BASE_URL}/tasks/candidates`);
    if (!response.ok) throw new Error('获取数据失败');
    return await response.json();
}

async function getBoardTasks() {
    const response = await fetch(`${BASE_URL}/tasks/?status=IN_PROGRESS`);
    if (!response.ok) throw new Error('获取看板失败');
    return await response.json();
}

async function confirmTaskById(id) {
    const response = await fetch(`${BASE_URL}/tasks/${id}/confirm`, { method: 'POST' });
    if (!response.ok) throw new Error('确认任务失败');
    return await response.json();
}

async function completeTaskById(id) {
    const response = await fetch(`${BASE_URL}/tasks/${id}/complete`, { method: 'POST' });
    if (!response.ok) throw new Error('标记完成失败');
    return await response.json();
}

async function deleteTaskById(id) {
    const response = await fetch(`${BASE_URL}/tasks/${id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('删除失败');
    return await response.json();
}

async function updateTask(id, taskData) {
    const response = await fetch(`${BASE_URL}/tasks/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData)
    });
    if (!response.ok) throw new Error('改写失败');
    return await response.json();
}

// 聊天发送请求
async function sendChatMessage(message) {
    const response = await fetch(`${BASE_URL}/tasks/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    });
    if (!response.ok) throw new Error('发送失败');
    return await response.json();
}