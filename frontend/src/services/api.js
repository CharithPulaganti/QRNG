import axios from 'axios'

export async function getBits(n) {
  const { data } = await axios.get(`/api/bits?n=${n}`)
  return data
}

export async function extractBits(bits, method) {
  const { data } = await axios.post('/api/extract', { bits, method })
  return data
}

export async function getReport(bits, block_size=128) {
  const { data } = await axios.post('/api/report', { bits, block_size })
  return data
}

export async function getKey(len=256, method='sha256') {
  const { data } = await axios.get(`/api/key?len=${len}&method=${method}`)
  return data
}
