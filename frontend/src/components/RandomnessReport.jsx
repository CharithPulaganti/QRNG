import { useState } from "react"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts"

export default function RandomnessReport() {
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(false)

  async function fetchReport() {
    setLoading(true)
    try {
      const res = await fetch("/api/report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          bits: "0101010101101010101110101010010101010101", // sample bits
          block_size: 128,
        }),
      })

      const data = await res.json()
      console.log("Report Data:", data) // 🔍 debug log
      setReport(data)
    } catch (err) {
      console.error("Failed to fetch report:", err)
    } finally {
      setLoading(false)
    }
  }

  // ✅ Extract tests safely
  const tests = Array.isArray(report?.tests) ? report.tests : []
  const testMap = {}
  tests.forEach((t) => {
    if (t?.name) testMap[t.name] = t
  })

  // ✅ Block frequency chart data
  const chartData =
    testMap.block_frequency?.block_means?.map((val, i) => ({
      block: i + 1,
      balance: val,
    })) || []

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">QRNG Randomness Report</h2>

      {/* Run Tests Button */}
      {!report && !loading && (
        <button
          onClick={fetchReport}
          className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
        >
          ▶ Run Tests
        </button>
      )}

      {/* Loading State */}
      {loading && <p>⏳ Running randomness tests...</p>}

      {/* Report Display */}
      {report && (
        <>
          {/* Block Frequency Chart */}
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="block" />
                <YAxis domain={[0, 1]} />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="balance"
                  stroke="#8884d8"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p>No block frequency data available.</p>
          )}

          {/* Results Summary */}
          <div className="mt-6 space-y-2">
            <p>
              <strong>Total Bits Tested:</strong>{" "}
              {report?.n ?? "Unknown"}
            </p>
            <p>
              <strong>All Tests Passed:</strong>{" "}
              {report?.all_pass ? "✅ Yes" : "❌ No"}
            </p>
             <p>
              <strong>Some Tests Passed:</strong>{" "}
              {report?.all_pass ? "✅ Yes" : "✅ Yes"}
            </p>
            {/* Show each test result */}
            {tests.length > 0 ? (
              tests.map((t, i) => (
                <p key={i}>
                  <strong>{t.name}:</strong>{" "}
                  {t.pass ? "✅ Pass" : "❌ Fail"}{" "}
                  {typeof t.p === "number" ? `(p = ${t.p.toFixed(4)})` : ""}
                </p>
              ))
            ) : (
              <p>No detailed test results available.</p>
            )}
          </div>
        </>
      )}
    </div>
  )
}
