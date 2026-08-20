import request from './request'

export const getMySignals = () => request.get('/signals/my')
export const getWaveform = (id) => request.get(`/signals/${id}/waveform`)
export const uploadSignal = (formData) => request.post('/signals/upload', formData)
