import React from 'react'
import { Trash2, ExternalLink, DollarSign } from 'lucide-react'

function SubscriptionCard({ subscription, onDelete }) {
  const formatCurrency = (amount, currency = 'USD') => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
    }).format(amount)
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-500'
      case 'cancelled':
        return 'bg-red-500'
      case 'expired':
        return 'bg-gray-500'
      default:
        return 'bg-blue-500'
    }
  }

  const displayCost = subscription.billing_cycle === 'yearly' 
    ? formatCurrency(subscription.yearly_cost, subscription.currency)
    : formatCurrency(subscription.monthly_cost, subscription.currency)

  const billingText = subscription.billing_cycle === 'yearly'
    ? `per year (${formatCurrency(subscription.monthly_cost, subscription.currency)}/mo)`
    : `per ${subscription.billing_cycle}`

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 shadow-xl hover:shadow-2xl transition-all duration-200 border border-white/20">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-white mb-1">{subscription.company}</h3>
          {subscription.service_name && (
            <p className="text-white/70 text-sm">{subscription.service_name}</p>
          )}
        </div>
        <span className={`${getStatusColor(subscription.status)} text-white text-xs px-2 py-1 rounded-full font-semibold`}>
          {subscription.status}
        </span>
      </div>

      <div className="space-y-3 mb-4">
        <div className="flex items-center gap-2">
          <DollarSign className="w-5 h-5 text-white/70" />
          <div>
            <p className="text-2xl font-bold text-white">{displayCost}</p>
            <p className="text-white/60 text-sm">{billingText}</p>
          </div>
        </div>

        {subscription.email && (
          <p className="text-white/70 text-sm truncate" title={subscription.email}>
            📧 {subscription.email}
          </p>
        )}

        {subscription.next_billing_date && (
          <p className="text-white/70 text-sm">
            📅 Next billing: {new Date(subscription.next_billing_date).toLocaleDateString()}
          </p>
        )}

        {subscription.notes && (
          <p className="text-white/60 text-sm italic">{subscription.notes}</p>
        )}
      </div>

      <div className="flex gap-2 pt-4 border-t border-white/20">
        {subscription.cancel_url && (
          <a
            href={subscription.cancel_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-colors duration-200 flex items-center justify-center gap-2 text-sm font-medium"
          >
            <ExternalLink className="w-4 h-4" />
            Cancel
          </a>
        )}
        <button
          onClick={() => onDelete(subscription.id)}
          className="px-4 py-2 bg-red-500/80 hover:bg-red-600 text-white rounded-lg transition-colors duration-200 flex items-center justify-center gap-2 text-sm font-medium"
        >
          <Trash2 className="w-4 h-4" />
          Remove
        </button>
      </div>
    </div>
  )
}

export default SubscriptionCard

