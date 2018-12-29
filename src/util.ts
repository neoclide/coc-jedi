import { CompletionItemKind } from 'vscode-languageserver-types'

export function convertType(type: string): CompletionItemKind {
  switch (type) {
    case 'class':
      return CompletionItemKind.Class
    case 'instance':
      return CompletionItemKind.Variable
    case 'lambda':
    case 'function':
      return CompletionItemKind.Function
    case 'module':
      return CompletionItemKind.Module
    case 'int':
    case 'float':
    case 'string':
    case 'boolean':
      return CompletionItemKind.Constant
    case 'method':
      return CompletionItemKind.Method
    case 'tuple':
      return CompletionItemKind.Enum
    case 'dict':
    case 'list':
      return CompletionItemKind.Variable
    default:
      return CompletionItemKind.Variable
  }
}
