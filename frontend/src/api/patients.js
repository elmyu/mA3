import request from './request'

export const getDoctorSchedules = () => request.get('/doctors/schedules')
export const getPatients = () => request.get('/patients')
export const getPatientSignals = (id) => request.get(`/patients/${id}/signals`)
