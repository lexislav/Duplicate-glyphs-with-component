#MenuTitle: Duplicate Glyph(s) with Component
# -*- coding: utf-8 -*-
__doc__="""
Duplicates selected glyphs but as components, giving them 001 suffix or above depending on availability.
Originaly based on Tache's script, but lately completely rewritten.
"""

import GlyphsApp

Font = Glyphs.font
FirstMasterID = Font.masters[0].id
selectedGlyphs = Font.selection

def removeSuffix(glyphName):
	#lets test for suffix existence
	try:
		dotIndex = glyphName.index('.')
	except:
		return glyphName
	#we know the suffix length amd position now
	suffixLength = len(glyphName) - glyphName.rindex('.')
	try:
		if glyphName[-suffixLength+1] == "0":
			return glyphName
		else:
			glyphName[:-suffixLength]
	except:
		return glyphName
	#it shouldnt end up here, but that was weaknes point of original script
	return glyphName

def findSuffix( glyphName ):
	glyphName = removeSuffix(glyphName)
	nameIsFree = False
	suffixNumber = 0
	while nameIsFree is False:
		suffixNumber += 1
		suffix = ".%03d" % suffixNumber
		if Font.glyphs[ glyphName+suffix ] == None:
			nameIsFree = True
		if suffixNumber == 100:
			break
	return suffix
	
def process( sourceGlyph ):
	sourceGlyphName = sourceGlyph.name
	targetSuffix = findSuffix( sourceGlyphName )
	# append suffix, create glyph:
	targetGlyphName = sourceGlyphName + targetSuffix
	targetGlyph = GSGlyph( targetGlyphName )
	Font.glyphs.append( targetGlyph )
	# place component from layers to layers in the new glyph:
	for thisLayer in sourceGlyph.layers:
		sourceComponent = GSComponent( sourceGlyphName )
		targetGlyph.layers[thisLayer.master.id].components.append(sourceComponent)
		targetGlyph.layers[thisLayer.master.id].width = sourceGlyph.layers[thisLayer.master.id].width
	print "Added", targetGlyphName 
	return

for thisGlyph in selectedGlyphs:
	process(thisGlyph)