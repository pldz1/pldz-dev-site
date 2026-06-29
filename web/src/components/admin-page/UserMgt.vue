<template>
  <div class="content-container">
    <div class="content-header">
      <h1>用户管理</h1>
      <p>查看并维护后台账号、权限与基础资料</p>
    </div>
    <div class="content-body">
      <div class="error-banner" v-if="errorMessage">{{ errorMessage }}</div>

      <div v-if="isLoading" class="loading-stack">
        <div v-for="n in 4" :key="`user-skeleton-${n}`" class="loading-card">
          <div class="skeleton-line w-25"></div>
          <div class="skeleton-line w-60" style="margin-top: 10px"></div>
          <div class="skeleton-line w-40" style="margin-top: 10px"></div>
        </div>
      </div>

      <div v-else-if="userMgt.users.length" class="list-block">
        <div class="list-row" v-for="(user, index) in userMgt.users" :key="user.username || index">
          <strong>#{{ index + 1 }} {{ user.nickname || user.username || "未命名用户" }}</strong>
          <div class="field">
            <span class="field-label">邮箱:</span>
            <span class="field-value">{{ user.username || "-" }}</span>
          </div>
          <div class="field">
            <span class="field-label">明文密码:</span>
            <span class="field-value field-value--muted">{{ user.raw_password || "-" }}</span>
          </div>
          <div class="field">
            <span class="field-label">管理员:</span>
            <span class="field-value">{{ user.isadmin ? "是" : "否" }}</span>
          </div>
          <div class="field">
            <span class="field-label">两步验证:</span>
            <span class="field-value">{{ user.two_factor_enabled ? "已开启" : "未开启" }}</span>
          </div>
          <div class="field field-grow">
            <span class="field-label">头像</span>
            <span class="field-value field-value--truncate" :title="user.avatar || '-'">{{ user.avatar || "-" }}</span>
          </div>
          <div class="inline-actions">
            <button class="btn btn-danger" @click="onDeleteUserByUsername(user.username)">删除</button>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">🧐</div>
        <p>暂无用户数据，稍后再试或刷新列表。</p>
        <button class="btn btn-outline" @click="refresh">重新加载</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getAllUsers, deleteUserByUsername } from "../../utils/apis";
import Toast from "../../utils/toast.js";
import { useLoading } from "../../utils/use-loading";

const errorMessage = ref("");
const userMgt = ref({ users: [] });
const { isLoading, start: startLoading, stop: stopLoading } = useLoading("admin.user.fetch");

async function fetchUsers({ showSuccessToast = false } = {}) {
  startLoading();
  try {
    const res = await getAllUsers();
    if (res?.data) {
      userMgt.value.users = res.data;
      errorMessage.value = "";
      if (showSuccessToast) {
        Toast.success("用户数据加载成功");
      }
      return true;
    }
    userMgt.value.users = [];
    errorMessage.value = "获取用户数据失败，请稍后再试";
    Toast.error("获取用户数据失败，请稍后再试");
    return false;
  } catch (error) {
    console.error("获取用户数据失败:", error);
    userMgt.value.users = [];
    errorMessage.value = "获取用户数据失败，请稍后再试";
    Toast.error("获取用户数据失败，请稍后再试");
    return false;
  } finally {
    stopLoading();
  }
}

async function onDeleteUserByUsername(username) {
  if (!username) return;
  if (!confirm(`确定要删除用户 ${username} 吗？`)) return;

  const res = await deleteUserByUsername(username);
  if (res) {
    Toast.success(`用户 ${username} 已删除`);
    await fetchUsers();
  } else {
    errorMessage.value = "删除用户失败，请稍后再试";
    Toast.error("删除用户失败，请稍后再试");
  }
}

function refresh() {
  fetchUsers({ showSuccessToast: true });
}

onMounted(async () => {
  await fetchUsers({ showSuccessToast: true });
});
</script>

<style scoped>
@import url("../../assets/components/admin-content.css");
</style>
