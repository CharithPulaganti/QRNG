import React, { useState } from 'react'
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts'
import { getBits, extractBits, getReport, getKey } from '../services/api'
import PValueTable from './PValueTable'

export default function Dashboard() {
  const [count, setCount] = useState(100000)
  const [bits, setBits] = useState('')
  const [note, setNote] = useState('')
  const [quantum, setQuantum] = useState(false)
  const [stats, setStats] = useState({})
  const [report, setReport] = useState(null)
  const [method, setMethod] = useState('sha256')
  const [postBits, setPostBits] = useState('')

  const calcStats = (s) => {
    const n = s.length
    const ones = (s.match(/1/g) || []).length
    const zeros = n - ones
    const freq = ones / n
    // rolling bias data downsampled
    const step = Math.max(1, Math.floor(n / 2000))
    const data = []
    let c1 = 0
    for (let i = 0; i < n; i++) {
      if (s[i] === '1') c1++
      if (i % step === 0) {
        data.push({ i, freq: c1 / (i + 1) })
      }
    }
    return { n, ones, zeros, freq, trend: data }
  }

  const handleGenerate = async () => {
    const res = await getBits(count)
    setBits(res.bits)
    setQuantum(res.quantum)
    setNote(res.note || '')
    setStats(calcStats(res.bits))
    setReport(null)
    setPostBits('')
  }

  const handleExtract = async () => {
    if (!bits) return
    const res = await extractBits(bits, method)
    setPostBits(res.bits)
  }

  const handleReport = async () => {
    if (!bits) return
    const rep = await getReport(bits, 128)
    setReport(rep)
  }

  const handleKey = async () => {
    const res = await getKey(256, 'sha256')
    alert(`256-bit key (hex):\n${res.hex}\nchecksum: ${res.checksum}`)
  }

  return (
    <div style={{ display: 'grid', gap: 16 }}>
      <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
        <input type="number" value={count} onChange={e => setCount(+e.target.value)} min={1000} max={5000000} />
        <button onClick={handleGenerate}>Generate Bits</button>
        <select value={method} onChange={e => setMethod(e.target.value)}>
          <option value="sha256">SHA-256 Extractor</option>
          <option value="von_neumann">Von Neumann</option>
        </select>
        <button onClick={handleExtract} disabled={!bits}>Apply Extractor</button>
        <button onClick={handleKey}>Generate 256-bit Key</button>
      </div>

      {note && <div style={{ background: '#fff3cd', padding: 8, border: '1px solid #ffeeba' }}>
        <b>Note:</b> {note}
      </div>}

      {stats.n && (
        <div>
          <p><b>Raw bits:</b> n={stats.n}, ones={stats.ones}, zeros={stats.zeros}, freq(1)={(stats.freq*100).toFixed(2)}%</p>
          <LineChart width={900} height={280} data={stats.trend}>
            <Line type="monotone" dataKey="freq" dot={false} />
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="i" />
            <YAxis domain={[0.45, 0.55]} />
            <Tooltip />
          </LineChart>
        </div>
      )}

      {postBits && (
        <div>
          <p><b>Post-processed bits length:</b> {postBits.length} (method: {method})</p>
        </div>
      )}

      {report && <PValueTable report={report} />}
    </div>
  )
}
