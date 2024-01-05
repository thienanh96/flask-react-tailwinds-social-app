import { store } from "./app/store"
import { NavBar } from "./common/components/NavBar"
import { PrimeReactProvider } from "primereact/api"
import { Provider } from "react-redux"
import Dashboard from "./features/dashboard/Dashboard"

// tailwind css
import "./global.css"

// primreact css
import "primereact/resources/themes/lara-light-indigo/theme.css" // theme
import "primeicons/primeicons.css"
import "primereact/resources/primereact.css" // core css
import "./App.css"

function App() {
  return (
    <PrimeReactProvider>
      <Provider store={store}>
        <div className="App bg-[#DAE0E6] h-lvh w-lvw overflow-auto">
          <NavBar />
          <Dashboard />
        </div>
      </Provider>
    </PrimeReactProvider>
  )
}

export default App
