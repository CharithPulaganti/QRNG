import React from 'react'

export default function PValueTable({ report }) {
  return (
    <div>
      <h3>Randomness Test Report</h3>
      <table border="1" cellPadding="6" style={{ borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>Test</th>
            <th>p-value</th>
            <th>Pass</th>
          </tr>
        </thead>
        <tbody>
          {report.tests.map((t, idx) => (
            <tr key={idx}>
              <td>{t.name}</td>
              <td>{typeof t.p === 'number' ? t.p.toFixed(6) : '-'}</td>
              <td>{String(t.pass)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p><b>All pass:</b> {String(report.all_pass)} | n = {report.n}</p>
    </div>
  )
}
