<template>
  <teleport to="body">
    <div class="auth-overlay" @click="onClickOverlay">
      <!-- 已经登录的卡片信息 -->
      <div v-if="!!username" class="info-card">
        <div class="auth-window-bar" aria-hidden="true">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="profile-panel">
          <div class="info-avatar">
            <img :src="avatar" alt="头像" />
            <button class="avatar-overlay" type="button" aria-label="上传头像" @click="onUploadAvatar($event)">+</button>
          </div>

          <div class="profile-copy">
            <div class="profile-title-row">
              <h2>{{ nickname || username }}</h2>
              <span class="role-badge">{{ isadmin ? "管理员" : "普通用户" }}</span>
            </div>
            <p>{{ username }}</p>
            <span class="security-pill">两步验证：{{ twoFactorEnabled ? "已开启" : "未开启" }}</span>
          </div>
        </div>

        <div class="profile-actions">
          <button v-if="isadmin" type="button" class="btn-profile-primary" @click="onOpenAdmin">进入后台</button>
          <button v-if="isadmin" type="button" class="btn-profile-secondary" @click="onOpenSecurity">账号安全</button>
          <button type="button" class="btn-profile-danger" @click="onLogout">退出登录</button>
        </div>
      </div>

      <!-- 登录/注册 表单 -->
      <div v-else class="auth-container">
        <div class="auth-window-bar" aria-hidden="true">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="auth-header">
          <h2>{{ showRegister ? "注册" : "登录" }}</h2>
          <div class="auth-close" @click="onCloseLoginForm"></div>
        </div>

        <!-- 错误提示 -->
        <div class="error">{{ error }}</div>
        <!-- 表单 -->
        <form method="post" @submit.prevent="onLoginOrRegister">
          <!-- 用户名 -->
          <input type="text" placeholder="邮箱地址(示例:user@example.com)" required v-model="name" @change="onCheckName" />
          <!-- 密码 -->
          <input type="password" placeholder="请输入密码" required v-model="pwd" />
          <input v-if="requiresTwoFactor && !showRegister" type="text" inputmode="numeric" autocomplete="one-time-code" placeholder="请输入 6 位两步验证码" required v-model="otpCode" />
          <!-- 昵称，仅在注册时显示 -->
          <input v-if="showRegister" type="text" placeholder="昵称" required v-model="nick" />
          <div class="action-buttons">
            <button type="button" class="btn-register" @click="onSwitchRegister">{{ showRegister ? "返回登录" : "注册" }}</button>
            <button type="submit" class="btn-login">{{ showRegister ? "注册" : "登录" }}</button>
          </div>
          <!-- 条款 -->
          <div class="agreement">
            注册/登录即表示同意 <a href="/api/v1/website/resource/user_agreement" target="_blank" rel="noopener noreferrer">用户协议</a> 和
            <a href="/api/v1/website/resource/privacy_policy" target="_blank" rel="noopener noreferrer">隐私政策</a>
          </div>
        </form>
      </div>
      <div class="auth-container flex-center loading" v-if="showLoginCss">
        <div class="my-loader"></div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { useStore } from "vuex";
import { useRouter } from "vue-router";

import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { login, register, logout, updateAvatar } from "../utils/apis";
import { uploadAvatar } from "../utils/file-upload.js";
import Toast from "../utils/toast.js";

const emit = defineEmits(["close-login-form"]);

// 引入 Vuex store
const store = useStore();
// 引入 Vue Router
const router = useRouter();

// 取用户头像
const avatar = computed(() => store.state.authState.avatar);
const username = computed(() => store.state.authState.username);
const nickname = computed(() => store.state.authState.nickname);
const isadmin = computed(() => store.state.authState.isadmin);
const twoFactorEnabled = computed(() => store.state.authState.twoFactorEnabled);

// 用户名和密码的响应式引用
const name = ref("");
const pwd = ref("");
const nick = ref("");
const ava = ref("");
const otpCode = ref("");
const error = ref("");
const requiresTwoFactor = ref(false);

// 显示是注册界面的状态
const showRegister = ref(false);

// 显示登陆css
const showLoginCss = ref(false);
let previousBodyOverflow = "";

/**
 * 检查用户名是否符合要求
 * @returns {boolean} 是否符合要求
 */
function onCheckName() {
  // 检查用户名是否符合要求
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailPattern.test(name.value)) {
    error.value = "请输入合法的邮箱地址（示例：user@example.com）";
    return false;
  } else {
    error.value = "";
    return true;
  }
}

/**
 * 切换注册界面
 */
function onSwitchRegister() {
  showRegister.value = !showRegister.value;
  requiresTwoFactor.value = false;
  otpCode.value = "";
}

async function updateAuthState(res) {
  await store.dispatch("authState/update", {
    username: res.username || "",
    isadmin: res.isadmin || false,
    avatar: res.avatar || "",
    nickname: res.nickname || "",
    two_factor_enabled: res.two_factor_enabled || false,
  });
}

/**
 * 登录或注册操作
 */
async function onLoginOrRegister() {
  showLoginCss.value = true;
  const isValid = onCheckName();
  if (!isValid) {
    showLoginCss.value = false;
    return;
  }

  // 如果是注册界面，则调用注册接口
  let res;
  if (showRegister.value) {
    res = await register(name.value, pwd.value, nick.value);
  } else {
    res = await login(name.value, pwd.value, otpCode.value);
  }

  if (res?.flag) {
    await updateAuthState(res);
    onCloseLoginForm();
    Toast.success("登录成功!");
  } else if (res?.requires_2fa) {
    requiresTwoFactor.value = true;
    error.value = res.log || "请输入两步验证码";
    Toast.error(error.value);
  } else {
    error.value = res?.log || "操作失败，请稍后再试";
    Toast.error(`登录失败: ${error.value}`);
  }
  showLoginCss.value = false;
}

/**
 * 退出操作
 */
async function onLogout() {
  await logout();
  await store.dispatch("authState/update", {
    username: "",
    avatar: "",
    nickname: "",
    isadmin: false,
    twoFactorEnabled: false,
  });
  onCloseLoginForm();
  Toast.success("退出成功!");
}

/**
 * 关闭登录表单
 */
function onCloseLoginForm() {
  emit("close-login-form");
}

/**
 * 处理点击遮罩事件
 * @param event
 */
function onClickOverlay(event) {
  // 点击遮罩时关闭登录表单
  if (event.target.classList.contains("auth-overlay")) {
    onCloseLoginForm();
  }
}

function onOpenAdmin() {
  if (isadmin.value) {
    router.push({ path: "/admin" });
    onCloseLoginForm();
  }
}

function onOpenSecurity() {
  if (isadmin.value) {
    router.push({ path: "/admin/security" });
    onCloseLoginForm();
  }
}

/**
 * 上传头像
 * @returns {Promise<void>}
 */
async function onUploadAvatar(event) {
  // 阻止事件冒泡，避免触发关闭登录表单
  event.stopPropagation();

  const res = await uploadAvatar(username.value);
  if (res?.data && res.data?.flag && res.data?.url) {
    ava.value = res.data.url;

    // 更新 中的头像
    await store.dispatch("authState/avatar", res.data.url);
    await updateAvatar(res.data.url);
  } else {
    error.value = "头像上传失败，请稍后再试";
  }
}

onMounted(() => {
  previousBodyOverflow = document.body.style.overflow || "";
  document.body.style.overflow = "hidden";
});

onBeforeUnmount(() => {
  document.body.style.overflow = previousBodyOverflow;
});
</script>

<style scoped>
.auth-overlay {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10030;
  min-height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(rgba(15, 23, 42, 0.62), rgba(15, 23, 42, 0.62)), linear-gradient(45deg, rgba(255, 255, 255, 0.08) 25%, transparent 25%),
    linear-gradient(-45deg, rgba(255, 255, 255, 0.08) 25%, transparent 25%);
  background-size: auto, 18px 18px, 18px 18px;
  overflow: auto;
  padding: 32px 18px;
}

.auth-container,
.info-card {
  position: relative;
  width: min(430px, 100%);
  margin: auto;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  background: #ffffff;
  box-shadow: 0 24px 70px rgba(15, 23, 42, 0.24);
  z-index: 10031;
}

.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading {
  position: absolute;
  inset: auto;
  min-height: 330px;
  z-index: 10032;
  background: rgba(255, 255, 255, 0.9);
}

.auth-window-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 30px;
  padding: 0 14px;
  border-bottom: 1px solid #e5edf6;
  background: #ffffff;
}

.auth-window-bar span {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #ffffff;
}

.auth-window-bar span:nth-child(1) {
  background: #ef4444;
}

.auth-window-bar span:nth-child(2) {
  background: #facc15;
}

.auth-window-bar span:nth-child(3) {
  background: #22c55e;
}

.auth-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 20px 22px 8px;
}

.auth-close {
  flex: 0 0 auto;
  height: 34px;
  width: 34px;
  border: 1px solid #dbe5f0;
  border-radius: 10px;
  background: #ffffff url("../assets/svgs/close-24.svg") no-repeat center;
  background-size: 18px;
  cursor: pointer;
}

.auth-close:hover {
  background-color: #f8fafc;
  border-color: #bfd4ff;
}

.auth-container h2 {
  margin: 0;
  color: #111827;
  font-size: 24px;
  line-height: 1.1;
  letter-spacing: 0;
}

.auth-container form {
  padding: 0 22px 22px;
}

.auth-container input {
  width: 100%;
  height: 44px;
  padding: 0 12px;
  margin: 10px 0 0;
  border: 1px solid #dbe5f0;
  border-radius: 12px;
  background: #f8fafc;
  color: #111827;
  font: inherit;
  box-shadow: none;
}

.auth-container input:focus {
  outline: none;
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.08);
}

.auth-container button {
  min-height: 42px;
  padding: 0 14px;
  margin-top: 0;
  border: 1px solid transparent;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 120ms ease, box-shadow 120ms ease, background-color 120ms ease;
}

.auth-container button:hover {
  transform: translateY(-1px);
}

.auth-container button:active {
  transform: translateY(0);
}

.action-buttons {
  display: flex;
  flex-direction: row;
  gap: 12px;
  margin-top: 16px;
}

.auth-container .btn-register {
  background: #fff;
  border-color: #dbe5f0;
  color: #334155;
}

.auth-container .btn-login {
  background: #2563eb;
  color: #ffffff;
  box-shadow: 0 10px 22px rgba(37, 99, 235, 0.16);
}

.auth-container .error {
  min-height: 22px;
  padding: 0 22px;
  color: #dc2626;
  font-size: 13px;
  font-weight: 700;
}

.auth-container .agreement {
  font-size: 12px;
  color: #475569;
  margin-top: 16px;
  line-height: 1.6;
}

.auth-container .agreement a {
  color: #2563eb;
  font-weight: 700;
  text-decoration: none;
}

.info-card {
  display: flex;
  flex-direction: column;
  gap: 18px;
  padding: 0 22px 22px;
}

.profile-panel {
  display: flex;
  align-items: center;
  gap: 16px;
  min-width: 0;
  padding-top: 22px;
}

.info-avatar {
  position: relative;
  width: 72px;
  height: 72px;
  border: 1px solid #dbe5f0;
  border-radius: 18px;
  overflow: hidden;
  flex-shrink: 0;
  background: #f8fafc;
}

.info-avatar img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  background: rgba(0, 0, 0, 0.4);
  color: #ffffff;
  border: none;
  opacity: 0;
  transition: opacity 0.2s ease;
  font-weight: 700;
  user-select: none;
  cursor: pointer;
}

.info-avatar:hover .avatar-overlay {
  opacity: 1;
}

.profile-copy {
  display: grid;
  gap: 7px;
  min-width: 0;
}

.profile-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.profile-title-row h2 {
  margin: 0;
  min-width: 0;
  overflow: hidden;
  color: #0f172a;
  font-size: 18px;
  font-weight: 750;
  line-height: 1.2;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-copy p {
  margin: 0;
  overflow: hidden;
  color: #64748b;
  font-size: 13px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.role-badge,
.security-pill {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  min-height: 26px;
  padding: 0 10px;
  border-radius: 999px;
  background: #eff6ff;
  color: #1d4ed8;
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
}

.security-pill {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #e2e8f0;
}

.profile-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.profile-actions button {
  min-height: 40px;
  padding: 0 13px;
  border: 1px solid transparent;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
}

.profile-actions button:hover {
  transform: translateY(-1px);
}

.btn-profile-primary {
  background: #2563eb;
  color: #ffffff;
  box-shadow: 0 10px 22px rgba(37, 99, 235, 0.16);
}

.btn-profile-secondary {
  background: #ffffff;
  border-color: #dbe5f0;
  color: #334155;
}

.btn-profile-danger {
  grid-column: 1 / -1;
  background: #fff1f2;
  border-color: #fecdd3;
  color: #be123c;
}

@media (max-width: 480px) {
  .auth-overlay {
    align-items: flex-start;
    padding-top: 92px;
  }

  .auth-header,
  .auth-container form {
    padding-left: 16px;
    padding-right: 16px;
  }

  .auth-container .error {
    padding-left: 16px;
    padding-right: 16px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .auth-container button {
    width: 100%;
  }

  .profile-panel {
    align-items: flex-start;
    flex-direction: column;
  }

  .profile-actions {
    grid-template-columns: 1fr;
  }

  .btn-profile-danger {
    grid-column: auto;
  }
}
</style>
