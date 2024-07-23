import { View, Text, ScrollView } from 'react-native'
import { Link } from 'expo-router'
import { SafeAreaView } from 'react-native-safe-area-context'
import {React, useState} from 'react'
import CustomButton from '../../components/CustomButton' 
import FormInput from '../../components/FormInput'
import GoogleAuth from '../../components/GoogleAuth'

const SignUp = () => {

  const [form, setForm] = useState({
    email: '', 
    password: '',
    username:''
  })


  return (
    <SafeAreaView className="bg-white h-full">
      <ScrollView>

        <View className="items-center">
          <FormInput 
            title="Email"
            value = {form.email}
            otherStyles = "mt-8"
            handleChangeText = {(e) => {setForm({...form, email: e})}}
            keyboardType = "email-address"
          />

          <FormInput 
            title="Username"
            otherStyles = "mt-8"
            value = {form.username}
            handleChangeText = {(e) => {setForm({...form, username: e})}}
          
          /> 
          <FormInput 
            title="Password"
            otherStyles = "mt-8"
            value = {form.password}
            handleChangeText = {(e) => {setForm({...form, password: e})}}
          
          /> 
          <CustomButton 
            title="Sign In"
            containerStyles="w-[85vw] mt-8"
          />
        </View>

        <View className="mt-8 ml-4">
          <Text>Already have an account? {' '}
          <Link
             href="/sign-in"
             className="text-lg font-semibold"
             >
              Sign In
            </Link>

            {' '} or
          </Text>
          <GoogleAuth />
        </View>
        


      </ScrollView>
    </SafeAreaView>
  )
}

export default SignUp