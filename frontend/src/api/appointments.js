import request from './request'

export const createAppointment = (data) => request.post('/appointments', data)
export const getMyAppointments = () => request.get('/appointments')
