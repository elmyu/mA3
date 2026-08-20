import request from './request'

export const getDevices = () => request.get('/devices')
export const updateDeviceStatus = (id, status) => request.put(`/devices/${id}/status`, { status })
export const createDevice = (data) => request.post('/devices', data)
export const updateDevice = (id, data) => request.put(`/devices/${id}`, data)
export const deleteDevice = (id) => request.delete(`/devices/${id}`)
