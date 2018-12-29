import { TextDocument, Position, CancellationToken, CompletionContext, CompletionItem, MarkupKind } from 'vscode-languageserver-protocol'
import fs from 'fs'
import pify from 'pify'
import Uri from 'vscode-uri'
import { JediCompleteItem } from '../types'
import { convertType } from '../util'
import { BaseProvider } from './base'
import { workspace, CompletionItemProvider } from 'coc.nvim'

export default class CompletionProvider extends BaseProvider implements CompletionItemProvider {

  public async provideCompletionItems(document: TextDocument, position: Position, _token: CancellationToken, _context: CompletionContext): Promise<CompletionItem[]> {
    const items: CompletionItem[] = []
    const doc = workspace.getDocument(document.uri)
    let filepath = Uri.parse(document.uri).fsPath
    if (filepath) {
      try {
        await pify(fs.stat)(filepath)
      } catch (e) {
        filepath = ''
      }
    }
    const col = Buffer.byteLength(doc.getline(position.line).slice(0, position.character))
    const content = document.getText()
    const res: JediCompleteItem[] = await this.request('completion', [position.line + 1, col, content, filepath])
    res.forEach(o => {
      this.debug('description:', o.description)
      let item = CompletionItem.create(o.name)
      item.kind = convertType(o.type)
      item.data = { index: o.index }
      if (o.docstring) {
        item.documentation = {
          kind: MarkupKind.Markdown,
          value: o.docstring
        }
      }
      items.push(item)
    })
    return items
  }

  public async resolveCompletionItem(item: CompletionItem): Promise<CompletionItem> {
    let { index } = item.data
    const res = await this.request('comletionResolve', [index])
    return item
  }
}
