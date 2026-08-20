<template>
  <view class="publish-page">
    <up-navbar title="发布原料" bg-color="#1e7e34" title-color="#fff" :auto-back="true" />

    <view class="form-area">
      <up-form :model="form">
        <up-form-item label="品类" required>
          <up-input v-model="form.type" placeholder="如：牛粪、鸡粪" />
        </up-form-item>
        <up-form-item label="重量(吨)" required>
          <up-input v-model="form.quantity" type="number" placeholder="预估重量" />
        </up-form-item>
        <up-form-item label="单价(元/吨)" required>
          <up-input v-model="form.price" type="digit" placeholder="期望单价" />
        </up-form-item>
        <up-form-item label="产地" required>
          <up-input v-model="form.location" placeholder="如：江苏省南京市江宁区" />
        </up-form-item>
        <up-form-item label="描述">
          <up-textarea v-model="form.description" placeholder="原料特点、用途等" />
        </up-form-item>
        <up-form-item label="含水率">
          <up-input v-model="form.moisture" placeholder="如：30%" />
        </up-form-item>
        <up-form-item label="有机质">
          <up-input v-model="form.organic_matter" placeholder="如：45%" />
        </up-form-item>
        <up-form-item label="现场图片">
          <up-upload :file-list="fileList" @after-read="afterRead" multiple :maxCount="6" />
          <text v-if="uploading" class="upload-hint">上传中...</text>
        </up-form-item>
      </up-form>

      <up-button type="primary" :loading="loading" @click="submit" block
                shape="circle" custom-style="margin-top:40rpx">提交审核</up-button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { createMaterial } from '@/api/materials'
import http from '@/api/request'

const form = reactive({
  type: '', quantity: '', price: '', location: '',
  description: '', moisture: '', organic_matter: ''
})
const fileList = ref([])
const uploadedUrls = ref([])
const uploading = ref(false)
const loading = ref(false)

/** 选择图片后实际上传到后端 */
async function afterRead(event) {
  const files = Array.isArray(event.file) ? event.file : [event.file]
  uploading.value = true
  for (const file of files) {
    try {
      const res = await http.upload('/api/upload', file.url)
      uploadedUrls.value.push(res.url)
      fileList.value.push({ url: BASE_URL + res.url })
    } catch (e) {
      uni.showToast({ title: '图片上传失败', icon: 'none' })
    }
  }
  uploading.value = false
}

// 拼接 BASE_URL（与 request.js 一致）
// #ifdef H5
const BASE_URL = 'http://127.0.0.1:5000'
// #endif
// #ifdef APP-PLUS
const BASE_URL = 'http://10.0.2.2:5000'
// #endif
// #ifndef H5 || APP-PLUS
const BASE_URL = 'http://127.0.0.1:5000'
// #endif

async function submit() {
  if (!form.type || !form.quantity || !form.price || !form.location) {
    uni.showToast({ title: '请填写必填项', icon: 'none' })
    return
  }
  loading.value = true
  try {
    await createMaterial({
      category_id: null,  // 由后端根据 type 名称匹配
      type: form.type,
      estimated_weight: parseFloat(form.quantity),
      price: parseFloat(form.price),
      province: form.location.split(' ')[0] || form.location,
      city: form.location.split(' ')[1] || '',
      detail_address: form.location,
      description: form.description,
      moisture_range: form.moisture,
      organic_matter: form.organic_matter,
      image_urls: uploadedUrls.value,
    })
    uni.showToast({ title: '发布成功，待审核', icon: 'success' })
    setTimeout(() => uni.navigateBack(), 1000)
  } catch (e) {} finally { loading.value = false }
}
</script>

<style scoped>
.publish-page { min-height: 100vh; background: #f5f5f5; }
.form-area { margin: 20rpx; background: #fff; border-radius: 16rpx; padding: 30rpx; }
.upload-hint { font-size:22rpx; color:#28a745; margin-top:8rpx; }
</style>
