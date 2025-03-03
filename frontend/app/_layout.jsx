import { View, Text } from 'react-native'
import { Stack } from 'expo-router'
import React from 'react'

const RootLayout = () => {
  return (
    <Stack>
        <Stack.Screen name="index" options={{headerShown: false}}/>
        <Stack.Screen name = "home"/>
        <Stack.Screen name="(auth)" options={{headerShown: false}}/>
    </Stack>
  )
}

export default RootLayout