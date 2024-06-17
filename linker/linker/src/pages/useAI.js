import{OpenAI} from 'openai'
const key = import.meta.env.VITE_OPENAI_KEY
const configuration={
    apiKey:key,
    dangerouslyAllowBrowser:true
}
const openai= new OpenAI(configuration)

export default openai