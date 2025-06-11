import React, { useState } from 'react'
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native'
import TextInput from '../components/TextInput'
import Button from '../components/Button'
import type { NativeStackNavigationProp } from '@react-navigation/native-stack'

type RootStackParamList = {
  Home: undefined
  'Upload Photo': undefined
  'Progress Graph': undefined
  Settings: undefined
  Login: undefined
  Signup: undefined
}

type SignupScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Signup'>
}

const BACKEND_URL = 'http://10.0.0.114:8000'

export default function SignupScreen({ navigation }: SignupScreenProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const handleSignup = async () => {
    if (loading) return
    setLoading(true)
    setError('')
    setSuccess(false)
    try {
      const res = await fetch(`${BACKEND_URL}/users/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, full_name: fullName })
      })
      if (!res.ok) {
        const data = await res.json()
        let errMsg = 'signup failed'
        if (typeof data.detail === 'string') {
          errMsg = data.detail
        } else if (Array.isArray(data.detail) && data.detail.length && data.detail[0].msg) {
          errMsg = data.detail[0].msg
        } else if (data.msg) {
          errMsg = data.msg
        }
        setError(errMsg)
        setLoading(false)
        return
      }
      setSuccess(true)
      setLoading(false)
      navigation.replace('Login')
    } catch (e) {
      setError('network error')
      setLoading(false)
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>sign up</Text>
      <TextInput
        value={fullName}
        onChangeText={setFullName}
        placeholder="full name"
        autoCapitalize="words"
      />
      <TextInput
        value={email}
        onChangeText={setEmail}
        placeholder="email"
        autoCapitalize="none"
      />
      <TextInput
        value={password}
        onChangeText={setPassword}
        placeholder="password"
        autoCapitalize="none"
        secureTextEntry
      />
      {error ? <Text style={styles.error}>{error}</Text> : null}
      {success ? <Text style={styles.success}>account created! please log in</Text> : null}
      <Button title={loading ? 'signing up...' : 'sign up'} onPress={handleSignup} />
      <TouchableOpacity onPress={() => navigation.replace('Login')} style={styles.linkContainer}>
        <Text style={styles.link}>already have an account? log in</Text>
      </TouchableOpacity>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24
  },
  title: {
    fontSize: 24,
    marginBottom: 24
  },
  error: {
    color: 'red',
    marginVertical: 8
  },
  success: {
    color: 'green',
    marginVertical: 8
  },
  linkContainer: {
    marginTop: 16
  },
  link: {
    color: '#222',
    textDecorationLine: 'underline'
  }
}) 