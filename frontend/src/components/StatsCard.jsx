import React from 'react'

function StatsCard({ title, value, icon }) {
  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 shadow-xl border border-white/20">
      <div className="flex items-center justify-between mb-2">
        <p className="text-white/70 text-sm font-medium">{title}</p>
        <div className="text-white/70">{icon}</div>
      </div>
      <p className="text-3xl font-bold text-white">{value}</p>
    </div>
  )
}

export default StatsCard

