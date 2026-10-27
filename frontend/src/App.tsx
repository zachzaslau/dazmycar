import { useEffect, useState } from 'react'

type ConnectionStatus = 'checking' | 'connected' | 'disconnected'

const connectionDisplay = {
  checking: { label: 'Checking backend connection…', color: 'bg-slate-400' },
  connected: { label: 'Backend connected', color: 'bg-emerald-600' },
  disconnected: { label: 'Backend disconnected', color: 'bg-red-600' },
} satisfies Record<ConnectionStatus, { label: string; color: string }>

export default function App() {
  const [connection, setConnection] = useState<ConnectionStatus>('checking')

  useEffect(() => {
    let disposed = false
    let pollTimer: ReturnType<typeof setTimeout> | undefined
    let activeRequest: AbortController | undefined

    async function checkConnection() {
      const controller = new AbortController()
      activeRequest = controller
      const timeout = setTimeout(() => controller.abort(), 3000)

      try {
        const response = await fetch('/api/v1/health', {
          signal: controller.signal,
          cache: 'no-store',
        })
        if (!response.ok) throw new Error('Health check failed')

        const health: unknown = await response.json()
        const connected =
          typeof health === 'object' &&
          health !== null &&
          'status' in health &&
          health.status === 'ok'

        if (!disposed) {
          setConnection(connected ? 'connected' : 'disconnected')
        }
      } catch {
        if (!disposed) setConnection('disconnected')
      } finally {
        clearTimeout(timeout)
        if (!disposed) pollTimer = setTimeout(checkConnection, 5000)
      }
    }

    void checkConnection()

    return () => {
      disposed = true
      clearTimeout(pollTimer)
      activeRequest?.abort()
    }
  }, [])

  const { label, color } = connectionDisplay[connection]

  return (
    <main className="mx-auto max-w-5xl px-6 py-16">
      <h1 className="text-4xl font-semibold">DAZ MY CAR!</h1>
      <p
        role="status"
        className="mt-8 flex items-center gap-2 text-sm text-slate-700"
      >
        <span
          aria-hidden="true"
          className={`size-2.5 rounded-full ${color}`}
        />
        {label}
      </p>
    </main>
  )
}
