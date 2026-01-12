import { ReactNode } from 'react'

interface LayoutProps {
  children: ReactNode
}

function Layout({ children }: LayoutProps) {
  return (
    <div className="layout">
      <header>
        <h1>NSW Estimation Software</h1>
        <p>New build - React UI</p>
      </header>
      <main>{children}</main>
    </div>
  )
}

export default Layout

