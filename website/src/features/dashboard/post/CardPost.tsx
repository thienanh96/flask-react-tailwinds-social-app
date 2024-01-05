import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"
import { Editor } from "primereact/editor"
import React, { useState } from "react"
import { Message } from "primereact/message"

interface CardPostProps {
  authorName: string
}

export default function CardPost({ authorName }: CardPostProps) {
  return (
    <div className="bg-white max-h-52 p-3">
      <p>{authorName}</p>
    </div>
  )
}
