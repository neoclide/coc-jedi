import { commands, ExtensionContext, languages, workspace } from 'coc.nvim'
import CompletionProvider from './features/completion'

export async function activate(context: ExtensionContext): Promise<void> {
  const { subscriptions } = context
  let config = workspace.getConfiguration('jedi')
  let enable = config.get<boolean>('enable', true)
  if (!enable) return

  let disposable = languages.registerCompletionItemProvider('jedi', 'JD', ['python'], new CompletionProvider(context), ['.'])
  subscriptions.push(disposable)

  subscriptions.push(commands.registerCommand('jedi.restart', () => {
    workspace.nvim.call('coc#jedi#restart', [], true)
  }))
}
