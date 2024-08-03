export type EnumTextChoice = {label: string, value: string}

export type EnumTextChoices = Record<string, EnumTextChoice>

export const EnumPublicChoices: EnumTextChoices =  {
  'public': {
    label: "Public (everyone)",
    value: "public"
  },
  'authenticated': {
    label: "Authenticated (logged in users)",
    value: "authenticated"
  },
  'emptya': {
    label: "Private (only me)",
    value: "emptya"
  }
}