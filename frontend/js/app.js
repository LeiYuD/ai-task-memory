// frontend/js/app.js

const { createApp, ref, onMounted } = Vue;

createApp({
    setup() {
        const tasks = ref([]);
        const loading = ref(true);
        const currentTab = ref('candidates'); // 'candidates' 或 'board'

        // 改写弹窗控制
        const showEditModal = ref(false);
        const editingTask = ref({ id: null, title: '', deadline: '' });

        // 配置弹窗控制
        const showConfigModal = ref(false);
        const configInfo = ref({ masked_email: '加载中...' });

        // 获取数据
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

        // 确认任务
        const confirmTask = async (id) => {
            try {
                await confirmTaskById(id);
                fetchTasks();
            } catch (e) { alert('操作失败'); }
        };

        // 标记完成
        const completeTask = async (id) => {
            try {
                await completeTaskById(id);
                fetchTasks();
            } catch (e) { alert('操作失败'); }
        };

        // 删除任务
        const deleteTask = async (id) => {
            if (!confirm('确定要忽略/删除这个任务吗？')) return;
            try {
                await deleteTaskById(id);
                fetchTasks();
            } catch (e) { alert('删除失败'); }
        };

        // 打开改写弹窗
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

        // 提交改写
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

        // 打开配置弹窗
        const openConfigModal = async () => {
            showConfigModal.value = true;
            try {
                const res = await fetch('http://127.0.0.1:8000/api/v1/settings/');
                configInfo.value = await res.json();
            } catch (e) {
                configInfo.value = { masked_email: '获取失败，请检查后端是否启动' };
            }
        };

        // 格式化时间
        const formatDate = (dateString) => {
            if (!dateString) return '';
            const d = new Date(dateString);
            const year = d.getFullYear();
            const month = (d.getMonth() + 1).toString().padStart(2, '0');
            const day = d.getDate().toString().padStart(2, '0');
            const hours = d.getHours().toString().padStart(2, '0');
            const minutes = d.getMinutes().toString().padStart(2, '0');

            // 返回格式：2026-11-21 15:30
            return `${year}-${month}-${day} ${hours}:${minutes}`;
        };

        // 页面加载时请求数据
        onMounted(() => {
            fetchTasks();
        });

        return {
            tasks, loading, currentTab, fetchTasks, confirmTask, deleteTask, completeTask,
            formatDate, showEditModal, editingTask, openEditModal, submitEdit,
            showConfigModal, configInfo, openConfigModal
        };
    }
}).mount('#app');