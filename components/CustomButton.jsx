import { View, Text, TouchableOpacity } from 'react-native'
import React from 'react'

const CustomButton = ({title, handlePress, containerStyles, textStyles, isLoading}) => {
  return (
    <TouchableOpacity 
        onPress = {handlePress}
        disabled = {isLoading}
        className={`bg-blue-500 rounded-lg min-h-[40px] items-center ${isLoading ? 'opacity-50' : ''} ${containerStyles}`}
    >
        <Text
            className={`font-bold text-lg color-white ${textStyles}`}
        >
            {title}
        </Text>
    </TouchableOpacity>
  )
}

export default CustomButton