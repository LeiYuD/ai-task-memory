// frontend/js/app.js

const { createApp, ref, onMounted } = Vue;

createApp({
    setup() {
        const tasks = ref([]);
        const loading = ref(true);

        // 弹窗控制变量
        const showEditModal = ref(false);
        const editingTask = ref({ id: null, title: '', deadline: '' });

        const fetchTasks = async () => {
            loading.value = true;
            try {
                tasks.value = await getCandidates();
            } catch (error) {
                console.error(error);
            } finally {
                loading.value = false;
            }
        };

        const confirmTask = async (id) => {
            try {
                await confirmTaskById(id);
                fetchTasks();
            } catch (e) {
                alert('操作失败');
            }
        };

        // 打开改写弹窗
        const openEditModal = (task) => {
            // 格式化时间以适配 datetime-local 输入框 (YYYY-MM-DDTHH:mm)
            let formattedDeadline = '';
            if (task.deadline) {
                // 解决时区偏移导致显示少一天/少一小时的问题
                const date = new Date(task.deadline);
                const offset = date.getTimezoneOffset() * 60000;
                const localISOTime = (new Date(date.getTime() - offset)).toISOString().slice(0, 16);
                formattedDeadline = localISOTime;
            }
            editingTask.value = {
                id: task.id,
                title: task.title,
                deadline: formattedDeadline
            };
            showEditModal.value = true;
        };

        // 提交修改
        const submitEdit = async () => {
            try {
                const updateData = { title: editingTask.value.title };
                if (editingTask.value.deadline) {
                    updateData.deadline = editingTask.value.deadline + ":00";
                }

                await updateTask(editingTask.value.id, updateData);
                showEditModal.value = false;
                fetchTasks();
            } catch (error) {
                alert('改写失败');
            }
        };

        const formatDate = (dateString) => {
            if (!dateString) return '';
            const d = new Date(dateString);
            return `${d.getMonth() + 1}月${d.getDate()}日 ${d.getHours()}:${d.getMinutes().toString().padStart(2, '0')}`;
        };

        onMounted(() => {
            fetchTasks();
        });

        return {
            tasks, loading, fetchTasks, confirmTask,
            formatDate, showEditModal, editingTask, openEditModal, submitEdit
        };
    }
}).mount('#app');