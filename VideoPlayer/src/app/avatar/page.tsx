'use client';

import { upload } from '@imagekit/next';
import Image from 'next/image';
import { useRef, useState } from 'react';
import '@/styles/avatar.css';

export default function AvatarUploadPage() {
  const inputFileRef = useRef<HTMLInputElement>(null);
  const [uploadedUrl, setUploadedUrl] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    const file = inputFileRef.current?.files?.[0];
    if (!file) {
      setError('Please select an image first.');
      return;
    }

    try {
      setIsUploading(true);
      setUploadedUrl(null);

      const authRes = await fetch('/api/upload-auth');
      const auth = await authRes.json();

      if (!authRes.ok) {
        throw new Error(auth?.error || 'Failed to get upload credentials.');
      }

      if (!auth?.publicKey) {
        throw new Error('Upload auth missing public key.');
      }

      if (!auth?.token || !auth?.signature || !auth?.expire) {
        throw new Error('Upload auth payload is incomplete.');
      }

      const result = await upload({
        file,
        fileName: file.name,
        folder: '/avatars',
        ...auth,
        publicKey: auth.publicKey,
      });

      if (!result?.url) {
        throw new Error('Avatar upload succeeded but no URL was returned.');
      }

      const saveRes = await fetch('/api/avatars', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filePath: result.filePath,
          fileName: result.name || file.name,
          url: result.url,
        }),
      });

      if (!saveRes.ok) {
        const body = await saveRes.json().catch(() => null);
        throw new Error(body?.error || 'Failed to save avatar record.');
      }

      setUploadedUrl(result.url);
    } catch (uploadError) {
      setError(uploadError instanceof Error ? uploadError.message : 'Upload failed.');
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <section className="avatar-page">
      <h1 className="page-title">Upload Your Avatar</h1>

      <form onSubmit={onSubmit} className="avatar-form">
        <label htmlFor="avatar-file">Avatar image</label>
        <input
          className="avatar-file-input"
          id="avatar-file"
          name="file"
          ref={inputFileRef}
          type="file"
          accept="image/jpeg, image/png, image/webp"
          required
        />
        <button type="submit" className="avatar-submit" disabled={isUploading}>
          {isUploading ? 'Uploading...' : 'Upload'}
        </button>
      </form>

      {error && <p className="avatar-error">{error}</p>}

      {uploadedUrl && (
        <div className="avatar-result">
          <p>
            <a href={uploadedUrl} target="_blank" rel="noreferrer">
              View uploaded avatar
            </a>
          </p>
          <Image src={uploadedUrl} alt="Uploaded avatar" className="avatar-preview" width={240} height={240} unoptimized />
        </div>
      )}
    </section>
  );
}