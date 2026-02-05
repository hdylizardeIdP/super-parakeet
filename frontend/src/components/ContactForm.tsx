import { useState, FormEvent } from "react";
import { submitContactInquiry } from "../api/client";

interface Props {
  propertyId: number;
  onClose: () => void;
}

export default function ContactForm({ propertyId, onClose }: Props) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<"idle" | "sending" | "sent" | "error">(
    "idle"
  );

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setStatus("sending");
    try {
      await submitContactInquiry({
        property_id: propertyId,
        name,
        email,
        phone: phone || undefined,
        message,
      });
      setStatus("sent");
    } catch {
      setStatus("error");
    }
  }

  if (status === "sent") {
    return (
      <div className="contact-success">
        <h3>Message Sent!</h3>
        <p>
          Thank you for your inquiry. We'll get back to you as soon as possible.
        </p>
        <button className="btn btn-secondary" onClick={onClose}>
          Close
        </button>
      </div>
    );
  }

  return (
    <form className="contact-form" onSubmit={handleSubmit}>
      <h3>Contact Agent</h3>
      <input
        type="text"
        placeholder="Your name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="email"
        placeholder="Email address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="tel"
        placeholder="Phone (optional)"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
      />
      <textarea
        placeholder="I'm interested in this property..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        rows={4}
        required
      />
      {status === "error" && (
        <p className="form-error">
          Something went wrong. Please try again.
        </p>
      )}
      <div className="form-actions">
        <button
          type="submit"
          className="btn btn-primary"
          disabled={status === "sending"}
        >
          {status === "sending" ? "Sending..." : "Send Message"}
        </button>
        <button type="button" className="btn btn-secondary" onClick={onClose}>
          Cancel
        </button>
      </div>
    </form>
  );
}
