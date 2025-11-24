import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Plus, Search, Trash2, Edit, DollarSign, Calendar, Zap } from 'lucide-react'
import SubscriptionCard from './components/SubscriptionCard'
import AddSubscriptionModal from './components/AddSubscriptionModal'
import StatsCard from './components/StatsCard'

const API_URL = 'http://localhost:8000/api'

function App() {
  const [subscriptions, setSubscriptions] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [showAddModal, setShowAddModal] = useState(false)
  const [stats, setStats] = useState(null)
  const [discovering, setDiscovering] = useState(false)

  useEffect(() => {
    fetchSubscriptions()
    fetchStats()
  }, [])

  const fetchSubscriptions = async () => {
    try {
      const response = await axios.get(`${API_URL}/subscriptions`)
      setSubscriptions(response.data)
    } catch (error) {
      console.error('Error fetching subscriptions:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/subscriptions/stats/summary`)
      setStats(response.data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const handleDiscover = async () => {
    setDiscovering(true)
    try {
      const response = await axios.post(`${API_URL}/subscriptions/discover`)
      alert(response.data.message)
      fetchSubscriptions()
      fetchStats()
    } catch (error) {
      console.error('Error discovering subscriptions:', error)
      alert('Error discovering subscriptions. Please try again.')
    } finally {
      setDiscovering(false)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to cancel this subscription?')) {
      try {
        await axios.delete(`${API_URL}/subscriptions/${id}`)
        fetchSubscriptions()
        fetchStats()
      } catch (error) {
        console.error('Error deleting subscription:', error)
        alert('Error cancelling subscription. Please try again.')
      }
    }
  }

  const handleAdd = async (subscriptionData) => {
    try {
      await axios.post(`${API_URL}/subscriptions`, subscriptionData)
      fetchSubscriptions()
      fetchStats()
      setShowAddModal(false)
    } catch (error) {
      console.error('Error adding subscription:', error)
      alert('Error adding subscription. Please try again.')
    }
  }

  const filteredSubscriptions = subscriptions.filter(sub =>
    sub.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (sub.service_name && sub.service_name.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-2">Subscription Manager</h1>
          <p className="text-white/80 text-lg">Track and manage all your subscriptions in one place</p>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <StatsCard
              title="Total Subscriptions"
              value={stats.total_subscriptions}
              icon={<DollarSign className="w-6 h-6" />}
            />
            <StatsCard
              title="Monthly Cost"
              value={`$${stats.total_monthly_cost.toFixed(2)}`}
              icon={<Calendar className="w-6 h-6" />}
            />
            <StatsCard
              title="Yearly Cost"
              value={`$${stats.total_yearly_cost.toFixed(2)}`}
              icon={<DollarSign className="w-6 h-6" />}
            />
            <StatsCard
              title="Est. Yearly"
              value={`$${stats.estimated_yearly.toFixed(2)}`}
              icon={<DollarSign className="w-6 h-6" />}
            />
          </div>
        )}

        {/* Actions Bar */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 mb-6 shadow-xl">
          <div className="flex flex-col md:flex-row gap-4 items-center">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search subscriptions..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-white/20 border border-white/30 rounded-lg text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50"
              />
            </div>
            <button
              onClick={handleDiscover}
              disabled={discovering}
              className="px-6 py-3 bg-gradient-to-r from-yellow-400 to-orange-500 text-white font-semibold rounded-lg hover:from-yellow-500 hover:to-orange-600 transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <Zap className="w-5 h-5" />
              {discovering ? 'Discovering...' : 'Auto-Discover'}
            </button>
            <button
              onClick={() => setShowAddModal(true)}
              className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl flex items-center gap-2"
            >
              <Plus className="w-5 h-5" />
              Add Subscription
            </button>
          </div>
        </div>

        {/* Subscriptions Grid */}
        {loading ? (
          <div className="text-center text-white text-xl py-12">Loading subscriptions...</div>
        ) : filteredSubscriptions.length === 0 ? (
          <div className="text-center text-white py-12">
            <p className="text-xl mb-4">No subscriptions found</p>
            <p className="text-white/70">Add a subscription or use auto-discover to find them automatically</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredSubscriptions.map((subscription) => (
              <SubscriptionCard
                key={subscription.id}
                subscription={subscription}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}

        {/* Add Subscription Modal */}
        {showAddModal && (
          <AddSubscriptionModal
            onClose={() => setShowAddModal(false)}
            onAdd={handleAdd}
          />
        )}
      </div>
    </div>
  )
}

export default App

