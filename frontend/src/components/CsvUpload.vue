<template>
  <div class="csv-upload">
    <el-upload :show-file-list="false" accept=".csv" :http-request="handleUpload" :disabled="uploading">
      <el-button type="success" plain :loading="uploading">上传 CSV 数据</el-button>
    </el-upload>
    <span class="hint">支持 UTF-8 编码的 .csv 文件，数值自动解析为信号数据</span>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadSignal } from '../api/signals'

const emit = defineEmits(['success'])
const uploading = ref(false)

async function handleUpload({ file }) {
  uploading.value = true
  try {
    const form = new FormData()
    form.append('file', file)
    form.append('signal_type', 'ECG')
    form.append('sample_rate', '250')
    await uploadSignal(form)
    ElMessage.success('上传成功')
    emit('success')
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
.csv-upload {
  display: flex;
  align-items: center;
  gap: 10px;
}
.hint {
  color: #6b7280;
  font-size: 12px;
}
</style>
