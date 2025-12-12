import { XCircle, CheckCircle, Loader2 } from 'lucide-react'

export default function StatusMessage({ type, title, message }) {
    const styles = {
        error: {
            bg: 'bg-red-50',
            border: 'border-red-200',
            icon: XCircle,
            iconColor: 'text-red-600',
            titleColor: 'text-red-900',
            messageColor: 'text-red-700'
        },
        success: {
            bg: 'bg-green-50',
            border: 'border-green-200',
            icon: CheckCircle,
            iconColor: 'text-green-600',
            titleColor: 'text-green-900',
            messageColor: 'text-green-700'
        },
        info: {
            bg: 'bg-blue-50',
            border: 'border-blue-200',
            icon: CheckCircle,
            iconColor: 'text-blue-600',
            titleColor: 'text-blue-900',
            messageColor: 'text-blue-700'
        }
    }

    const style = styles[type] || styles.info
    const Icon = style.icon

    return (
        <div className={`mt-6 ${style.bg} border ${style.border} rounded-lg p-4 flex items-start gap-3`}>
            <Icon className={`h-5 w-5 ${style.iconColor} flex-shrink-0 mt-0.5`} />
            <div>
                <h3 className={`font-medium ${style.titleColor}`}>{title}</h3>
                <p className={`${style.messageColor} text-sm mt-1`}>{message}</p>
            </div>
        </div>
    )
}
