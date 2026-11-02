import { useState } from 'react'
import './CarCard.css'

type CarProperties = {
    imageUrl: string
    year: number
    make: string
    model: string
    mileage: number
    isNew: boolean
    priceCents: number
    transmission: string
    fuelType: string
    drivetrain: string
}

const transmissionLabels: Record<string, string> = {
    A: 'Automatic',
    M: 'Manual',
    CVT: 'Automatic',
    'Dual Clutch': 'Automatic'
}

const fuelLabels: Record<string, string> = {
    'Flex Fuel Vehicle': 'Gasoline',
    Biodiesel: 'Diesel',
}

export default function CarCard({
        imageUrl,
        year,
        make,
        model,
        mileage,
        isNew,
        priceCents,
        transmission,
        fuelType,
        drivetrain,
    }: CarProperties ) {
        const title = `${year} ${make} ${model}`
        const [photoFailed, setPhotoFailed] = useState(false)

        return (
            <div className = "car-card">
                <div className = "car-card-media">
                    <img 
                        className = {photoFailed ? 'car-card-image car-card-image-default' : 'car-card-image' }
                        src = {photoFailed ? '/default-car.png' : imageUrl }
                        alt = {title}
                        onError = { () => setPhotoFailed(true) }
                    />
                    <span className = "car-card-tag">{isNew ? 'New' : 'Used'}</span>
                </div>
                <div className = "car-card-body">
                    <h2 className = "car-card-title">{title}</h2>
                    <p className = "car-card-price">{(priceCents / 100).toLocaleString('en-US', {
                            style: 'currency',
                            currency: 'USD',
                            maximumFractionDigits: 2
                        })}
                    </p>
                    <p className = "car-card-mileage">
                        {mileage.toLocaleString()} miles
                    </p>
                    <div className = "car-card-specs">
                        <span>
                            <img src = "/gearbox.svg" alt = "" />
                            {transmissionLabels[transmission]}
                        </span>
                        <span>
                            <img src = "/fuel.svg" alt = "" />
                            {fuelLabels[fuelType] ?? fuelType }
                        </span>
                        <span>
                            <img src = "/wheel.svg" alt = "" />
                            {drivetrain}
                        </span>
                    </div>
                </div>
            </div>
        )
    }