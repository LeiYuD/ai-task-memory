// frontend/js/app.js

const { createApp, ref, onMounted, nextTick } = Vue;

createApp({
    setup() {
        const tasks = ref([]);
        const loading = ref(true);
        const currentTab = ref('candidates');

        // 改写弹窗
        const showEditModal = ref(false);
        const editingTask = ref({ id: null, title: '', deadline: '' });

        // 配置弹窗
        const showConfigModal = ref(false);
        const configInfo = ref({ masked_email: '加载中...' });

        // 聊天窗口
        const showChat = ref(false);
        const chatInput = ref('');
        const chatLoading = ref(false);
        const chatHistory = ref([]);

        const fetchTasks = async () => {
            loading.value = true;
            try {
                if (currentTab.value === 'candidates') {
                    tasks.value = await getCandidates();
                } else {
                    tasks.value = await getBoardTasks();
                }
            } catch (error) {
                console.error("获取数据失败:", error);
            } finally {
                loading.value = false;
            }
        };

        const confirmTask = async (id) => {
            try {
                await confirmTaskById(id);
                fetchTasks();
            } catch (e) { alert('操作失败'); }
        };

        const completeTask = async (id) => {
            try {
                await completeTaskById(id);
                fetchTasks();
            } catch (e) { alert('操作失败'); }
        };

        const deleteTask = async (id) => {
            if (!confirm('确定要忽略/删除这个任务吗？')) return;
            try {
                await deleteTaskById(id);
                fetchTasks();
            } catch (e) { alert('删除失败'); }
        };

        const openEditModal = (task) => {
            let formattedDeadline = '';
            if (task.deadline) {
                const date = new Date(task.deadline);
                const offset = date.getTimezoneOffset() * 60000;
                formattedDeadline = (new Date(date.getTime() - offset)).toISOString().slice(0, 16);
            }
            editingTask.value = { id: task.id, title: task.title, deadline: formattedDeadline };
            showEditModal.value = true;
        };

        const submitEdit = async () => {
            try {
                const updateData = { title: editingTask.value.title };
                if (editingTask.value.deadline) {
                    updateData.deadline = editingTask.value.deadline + ":00";
                }
                await updateTask(editingTask.value.id, updateData);
                showEditModal.value = false;
                fetchTasks();
            } catch (error) { alert('改写失败'); }
        };

        const openConfigModal = async () => {
            showConfigModal.value = true;
            try {
                const res = await fetch('http://127.0.0.1:8000/api/v1/settings/');
                configInfo.value = await res.json();
            } catch (e) {
                configInfo.value = { masked_email: '获取失败，请检查后端' };
            }
        };

        // 发送聊天消息
        const sendChat = async () => {
            if (!chatInput.value.trim()) return;

            const userMsg = chatInput.value;
            chatHistory.value.push({ role: 'user', content: userMsg });
            chatInput.value = '';
            chatLoading.value = true;

            // 自动滚动到底部
            nextTick(() => {
                const box = document.getElementById('chat-box');
                if (box) box.scrollTop = box.scrollHeight;
            });

            try {
                const res = await sendChatMessage(userMsg);
                chatHistory.value.push({ role: 'ai', content: res.reply });

                // 如果 AI 成功提取了任务，自动刷新后台看板数据
                if (res.has_task) {
                    fetchTasks();
                }
            } catch (error) {
                chatHistory.value.push({ role: 'ai', content: '网络出小差了，请稍后再试。' });
            } finally {
                chatLoading.value = false;
                // 再次滚动到底部
                nextTick(() => {
                    const box = document.getElementById('chat-box');
                    if (box) box.scrollTop = box.scrollHeight;
                });
            }
        };

        const formatDate = (dateString) => {
            if (!dateString) return '';
            const d = new Date(dateString);
            const year = d.getFullYear();
            const month = (d.getMonth() + 1).toString().padStart(2, '0');
            const day = d.getDate().toString().padStart(2, '0');
            const hours = d.getHours().toString().padStart(2, '0');
            const minutes = d.getMinutes().toString().padStart(2, '0');
            return `${year}-${month}-${day} ${hours}:${minutes}`;
        };

        onMounted(() => {
            fetchTasks();
        });

        return {
            tasks, loading, currentTab, fetchTasks, confirmTask, deleteTask, completeTask,
            formatDate, showEditModal, editingTask, openEditModal, submitEdit,
            showConfigModal, configInfo, openConfigModal,
            showChat, chatInput, chatLoading, chatHistory, sendChat
        };
    }
}).mount('#app');