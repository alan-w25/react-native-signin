import { StatusBar } from 'expo-status-bar';
import { Text, View, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import CustomButton from '../components/CustomButton';
import { router } from 'expo-router';


export default function App() {

  return (
    <SafeAreaView>
        <ScrollView className="h-full">
            <Text className="text-4xl px-4">Hello</Text>
            <View className="items-center">
                <CustomButton 
                    title="Press Me"
                    handlePress = { () => { router.push('sign-in')}}
                    containerStyles = "w-[85vw] mt-8"
                />
            </View>
            
        </ScrollView>
    </SafeAreaView>
  );
}