import axios from 'axios'

/* -----------------------------
   JSON APIs (Axios)
----------------------------- */

export async function getBits(n) {
  const { data } = await axios.get(`/api/bits?n=${n}`)
  return data
}

export async function extractBits(bits, method) {
  const { data } = await axios.post('/api/extract', { bits, method })
  return data
}

export async function getReport(bits, block_size = 128) {
  const { data } = await axios.post('/api/report', { bits, block_size })
  return data
}

export async function getKey(len = 256, method = 'sha256') {
  const { data } = await axios.get(`/api/key?len=${len}&method=${method}`)
  return data
}

/* -----------------------------
   FILE DOWNLOAD APIs (NO AXIOS)
----------------------------- */

export function downloadRawBits(n = 1024) {
  window.open(`/api/download/raw/txt?n=${n}`, '_blank')
}

export function downloadFinalTxt(n = 1024, method = 'sha256') {
  window.open(`/api/download/final/txt?n=${n}&method=${method}`, '_blank')
}

export function downloadFinalBin(n = 1024, method = 'sha256') {
  window.open(`/api/download/final/bin?n=${n}&method=${method}`, '_blank')
}
