<template>
  <view class="register-page">
    <up-navbar title="注册" bg-color="#1e7e34" title-color="#fff" :auto-back="true" />

    <view class="form-area">
      <up-form :model="form" ref="formRef" :rules="rules">
        <up-form-item prop="username" label="用户名" border-bottom>
          <up-input v-model="form.username" placeholder="请输入用户名" />
        </up-form-item>
        <up-form-item prop="password" label="密码" border-bottom>
          <up-input v-model="form.password" type="password" placeholder="请输入密码" />
        </up-form-item>
        <up-form-item prop="email" label="邮箱" border-bottom>
          <up-input v-model="form.email" placeholder="请输入邮箱" />
        </up-form-item>
        <up-form-item prop="phone" label="手机号" border-bottom>
          <up-input v-model="form.phone" type="number" placeholder="请输入手机号" />
        </up-form-item>
        <up-form-item prop="role" label="角色" border-bottom>
          <up-radio-group v-model="form.role" placement="row">
            <up-radio v-for="(item, idx) in roles" :key="idx" :label="item.label" :name="item.value" />
          </up-radio-group>
        </up-form-item>
        <up-form-item v-if="form.role==='supplier'" prop="company" label="公司/农场" border-bottom>
          <up-input v-model="form.company" placeholder="选填" />
        </up-form-item>
        <up-form-item v-if="form.role==='supplier'" prop="address" label="地址" border-bottom>
          <up-input v-model="form.address" placeholder="选填" />
        </up-form-item>
      </up-form>

      <up-button type="primary" :loading="loading" @click="handleRegister" block
                shape="circle" custom-style="margin-top:40rpx">注册</up-button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const form = reactive({
  username: '', password: '', email: '', phone: '', role: 'farmer',
  company: '', address: ''
})

const roles = [
  { label: '农户', value: 'farmer' },
  { label: '供应商', value: 'supplier' },
]

const rules = {
  username: { type: 'string', required: true, message: '请输入用户名' },
  password: { type: 'string', required: true, min: 4, message: '密码至少4位' },
  email: { type: 'string', required: true, message: '请输入邮箱' },
  phone: { type: 'string', required: true, pattern: /^1[3-9]\d{9}$/, message: '手机号格式错误' },
}

const loading = ref(false)

async function handleRegister() {
  if (!form.username || !form.password || !form.email || !form.phone) {
    uni.showToast({ title: '请填写必填项', icon: 'none' })
    return
  }
  loading.value = true
  try {
    // 先注册
    await userStore.register(form)
    // 注册成功后自动登录
    await userStore.login(form.username, form.password)
    uni.showToast({ title: '注册成功', icon: 'success' })
    setTimeout(() => uni.switchTab({ url: '/pages/index/index' }), 800)
  } catch (e) {
    // error handled in request.js
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page { min-height: 100vh; background: #f5f5f5; }
.form-area { padding: 30rpx; background: #fff; margin: 20rpx; border-radius: 16rpx; }
</style>
