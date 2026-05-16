import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'
import { getPosts, suggestSubjects, generatePost } from '../services/api'

function Dashboard() {
  const { user, logout } = useAuth()
  const queryClient = useQueryClient()

  const [subjects, setSubjects] = useState([])
  const [selectedSubject, setSelectedSubject] = useState('')
  const [tone, setTone] = useState('professional')
  const [generatedPost, setGeneratedPost] = useState(null)

  // Récupère la liste des posts
  const { data: posts, isLoading: postsLoading } = useQuery({
    queryKey: ['posts'],
    queryFn: () => getPosts().then(res => res.data)
  })

  // Mutation pour suggérer des sujets
  const suggestMutation = useMutation({
    mutationFn: () => suggestSubjects().then(res => res.data),
    onSuccess: (data) => setSubjects(data.subjects)
  })

  // Mutation pour générer un post
  const generateMutation = useMutation({
    mutationFn: () => generatePost(selectedSubject, tone).then(res => res.data),
    onSuccess: (data) => {
      setGeneratedPost(data)
      queryClient.invalidateQueries(['posts'])
    }
  })

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Bonjour {user?.username} 👋</h1>
        <button onClick={logout}>Se déconnecter</button>
      </div>

      {/* Section suggestions */}
      <div style={{ marginBottom: '2rem', padding: '1.5rem', border: '1px solid #eee', borderRadius: '8px' }}>
        <h2>1. Choisir un sujet</h2>
        <button
          onClick={() => suggestMutation.mutate()}
          disabled={suggestMutation.isPending}
        >
          {suggestMutation.isPending ? 'Génération...' : '✨ Suggérer des sujets'}
        </button>

        {subjects.length > 0 && (
          <div style={{ marginTop: '1rem' }}>
            {subjects.map((subject, index) => (
              <div
                key={index}
                onClick={() => setSelectedSubject(subject)}
                style={{
                  padding: '0.75rem',
                  margin: '0.5rem 0',
                  border: selectedSubject === subject ? '2px solid blue' : '1px solid #ddd',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  background: selectedSubject === subject ? '#f0f4ff' : 'white'
                }}
              >
                {subject}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Section génération */}
      {selectedSubject && (
        <div style={{ marginBottom: '2rem', padding: '1.5rem', border: '1px solid #eee', borderRadius: '8px' }}>
          <h2>2. Générer le post</h2>
          <p><strong>Sujet :</strong> {selectedSubject}</p>

          <div style={{ marginBottom: '1rem' }}>
            <label>Ton du post : </label>
            <select value={tone} onChange={(e) => setTone(e.target.value)}>
              <option value="professional">Professionnel</option>
              <option value="storytelling">Storytelling</option>
              <option value="hot_take">Hot Take</option>
            </select>
          </div>

          <button
            onClick={() => generateMutation.mutate()}
            disabled={generateMutation.isPending}
          >
            {generateMutation.isPending ? 'Génération en cours...' : '🚀 Générer le post'}
          </button>
        </div>
      )}

      {/* Post généré */}
      {generatedPost && (
        <div style={{ marginBottom: '2rem', padding: '1.5rem', border: '1px solid #eee', borderRadius: '8px' }}>
          <h2>3. Ton post LinkedIn</h2>
          <textarea
            value={generatedPost.content}
            rows={10}
            style={{ width: '100%', padding: '1rem', fontSize: '14px' }}
            readOnly
          />
          <button
            onClick={() => navigator.clipboard.writeText(generatedPost.content)}
            style={{ marginTop: '0.5rem' }}
          >
            📋 Copier le post
          </button>
        </div>
      )}

      {/* Liste des posts sauvegardés */}
      <div style={{ padding: '1.5rem', border: '1px solid #eee', borderRadius: '8px' }}>
        <h2>Mes posts sauvegardés</h2>
        {postsLoading ? (
          <p>Chargement...</p>
        ) : posts?.length === 0 ? (
          <p>Aucun post pour l'instant</p>
        ) : (
          posts?.map(post => (
            <div key={post.id} style={{ padding: '1rem', margin: '0.5rem 0', background: '#f9f9f9', borderRadius: '6px' }}>
              <strong>{post.subject}</strong>
              <span style={{ marginLeft: '1rem', color: '#888', fontSize: '12px' }}>{post.status}</span>
              <p style={{ marginTop: '0.5rem', fontSize: '13px', color: '#555' }}>
                {post.content?.substring(0, 100)}...
              </p>
            </div>
          ))
        )}
      </div>

    </div>
  )
}

export default Dashboard